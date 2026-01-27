import logging
import os
import json

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

BASE_URL = "https://www.tenderned.nl/papi/tenderned-rs-tns/v2"


def create_session(username: str, password: str) -> requests.Session:
    """Create a session with the basic auth headers included."""
    session = requests.Session()
    session.auth = (username, password)
    return session


def find_publication_with_xml(session: requests.Session, max_attempts: int = 20) -> int:
    """Find a publication that has XML export available.
    
    Args:
        session: authenticated session
        max_attempts: maximum number of publications to check
        
    Returns:
        int: publication ID with XML available
    """
    url = f"{BASE_URL}/publicaties"
    logging.info(f"Searching for publications with XML export...")
    
    params = {'size': max_attempts}
    response = session.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    publications = data.get('content', [])
    
    for pub in publications:
        pub_id = int(pub['publicatieId'])
        pub_type = pub.get('typePublicatie', {}).get('omschrijving', 'Unknown')
        pub_name = pub.get('aanbestedingNaam', 'No name')[:50]
        
        # Try to get XML
        xml_url = f"{BASE_URL}/publicaties/{pub_id}/public-xml"
        try:
            xml_response = session.get(xml_url, timeout=5)
            if xml_response.status_code == 200 and xml_response.text:
                logging.info(f"✓ Found publication with XML: {pub_id} - {pub_type} - {pub_name}")
                return pub_id
            else:
                logging.debug(f"✗ No XML for {pub_id} - {pub_type}")
        except Exception as e:
            logging.debug(f"✗ Error checking {pub_id}: {e}")
    
    raise ValueError(f"No publications with XML found in {max_attempts} attempts")


def call_tns_xml_api(session: requests.Session, pub_id: int) -> str:
    """Call the TenderNed Notice Service XML API endpoint."""
    url = f"{BASE_URL}/publicaties/{pub_id}/public-xml"
    logging.info(f"Retrieving XML data from {url}")
    
    response = session.get(url)
    response.raise_for_status()
    return response.text


def parse_response(response_text: str) -> None:
    """Parses the raw response text retrieved from the XML API."""
    soup = BeautifulSoup(response_text, features="xml")
    
    logging.info(f"XML Response length: {len(response_text)} characters")
    logging.info(f"Root element: {soup.find().name if soup.find() else 'None'}")

    # Try to find common elements
    object_contract = soup.find("OBJECT_CONTRACT")
    if object_contract:
        contract_title = object_contract.find("TITLE")
        if contract_title:
            logging.info(f"Contract title: {contract_title.get_text(strip=True)}")
            return
    
    # Alternative: check for other common elements
    title_tags = soup.find_all("TITLE")
    if title_tags:
        logging.info(f"Found {len(title_tags)} TITLE elements:")
        for i, title in enumerate(title_tags[:3], 1):
            logging.info(f"  {i}. {title.get_text(strip=True)[:100]}")
    else:
        logging.info("No standard OBJECT_CONTRACT/TITLE structure found")
        logging.info(f"XML preview: {response_text[:500]}")


def main() -> None:
    """Example to retrieve and parse a single eForms publication."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

    load_dotenv()
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
    if not username or not password:
        logging.error("Please provide a username and password in the .env file.")
        return

    session = create_session(username, password)
    
    try:
        # Find a publication with XML available
        pub_id = find_publication_with_xml(session)
        
        # Get and parse the XML
        resp = call_tns_xml_api(session, pub_id=pub_id)
        parse_response(resp)
        
        logging.info("\n✓ Successfully retrieved and parsed publication XML")
        
    except Exception as e:
        logging.error(f"Failed: {e}")


if __name__ == "__main__":
    main()
