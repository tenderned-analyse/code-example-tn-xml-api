import logging
import os
import json
from typing import Dict, List, Any

import requests
from dotenv import load_dotenv

BASE_URL = "https://www.tenderned.nl/papi/tenderned-rs-tns/v2"


def create_session(username: str, password: str) -> requests.Session:
    """Create a session with the basic auth headers included.

    Args:
        username: username used to authenticate the requests
        password: password used to authenticate the requests

    Returns:
        requests.Session: authenticated session
    """
    session = requests.Session()
    session.auth = (username, password)
    return session


def get_publications(session: requests.Session, size: int = 10) -> List[Dict[str, Any]]:
    """Get recent publications from the API.
    
    Args:
        session: authenticated session
        size: number of publications to retrieve
        
    Returns:
        List of publication dictionaries
    """
    url = f"{BASE_URL}/publicaties"
    logging.info(f"Fetching {size} publications from {url}")
    
    params = {'size': size}
    response = session.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    publications = data.get('content', [])
    
    logging.info(f"Retrieved {len(publications)} publications")
    return publications


def get_publication_details(session: requests.Session, pub_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific publication.
    
    Args:
        session: authenticated session
        pub_id: publication ID
        
    Returns:
        Publication details dictionary
    """
    url = f"{BASE_URL}/publicaties/{pub_id}"
    logging.info(f"Fetching details for publication {pub_id}")
    
    response = session.get(url)
    response.raise_for_status()
    
    return response.json()


def display_publication_summary(pub: Dict[str, Any]) -> None:
    """Display a summary of a publication.
    
    Args:
        pub: publication dictionary
    """
    pub_id = pub.get('publicatieId', 'N/A')
    
    # Handle different typePublicatie formats
    pub_type_data = pub.get('typePublicatie', {})
    if isinstance(pub_type_data, dict):
        pub_type = pub_type_data.get('omschrijving', 'Unknown')
    else:
        pub_type = str(pub_type_data)
    
    pub_date = pub.get('publicatieDatum', 'N/A')
    name = pub.get('aanbestedingNaam', 'No name')
    
    logging.info(f"\n{'='*80}")
    logging.info(f"Publication ID: {pub_id}")
    logging.info(f"Type: {pub_type}")
    logging.info(f"Date: {pub_date}")
    logging.info(f"Name: {name}")
    
    # Display aankondiging info if available
    aankondiging = pub.get('aankondiging', {})
    if aankondiging and isinstance(aankondiging, dict):
        org = aankondiging.get('aanbestedende_dienst', {}).get('naam_aanbestedende_dienst', 'N/A')
        logging.info(f"Organization: {org}")
        
        sluit_datum = aankondiging.get('termijnen', {}).get('datum_sluiting_aanmelding', 'N/A')
        if sluit_datum:
            logging.info(f"Closing date: {sluit_datum}")
    
    logging.info(f"{'='*80}")


def display_detailed_publication(pub: Dict[str, Any]) -> None:
    """Display detailed information about a publication.
    
    Args:
        pub: publication dictionary
    """
    logging.info(f"\n{'='*80}")
    logging.info("DETAILED PUBLICATION INFORMATION")
    logging.info(f"{'='*80}")
    
    # Basic info
    display_publication_summary(pub)
    
    # Additional details
    aankondiging = pub.get('aankondiging', {})
    if aankondiging:
        logging.info("\n--- Tender Details ---")
        
        # Description
        beschrijving = aankondiging.get('beschrijving_opdracht', {})
        if beschrijving:
            korte_beschrijving = beschrijving.get('korte_beschrijving', 'N/A')
            logging.info(f"Description: {korte_beschrijving[:200]}...")
        
        # Procedures
        procedures = aankondiging.get('procedures', {})
        if procedures:
            proc_type = procedures.get('soort_procedure', 'N/A')
            logging.info(f"Procedure type: {proc_type}")
        
        # CPV codes
        cpv_codes = aankondiging.get('cpv_codes', [])
        if cpv_codes:
            logging.info(f"CPV codes: {', '.join([c.get('code', '') for c in cpv_codes[:3]])}")
    
    # Documents
    documenten = pub.get('documenten', [])
    if documenten:
        logging.info(f"\n--- Documents ({len(documenten)}) ---")
        for i, doc in enumerate(documenten[:5], 1):
            doc_naam = doc.get('naam', 'Unknown')
            doc_type = doc.get('type', 'Unknown')
            logging.info(f"{i}. {doc_naam} ({doc_type})")


def main() -> None:
    """Example to retrieve and display TenderNed publications using JSON API.

    Steps:
    1. Retrieve authentication information from .env file
    2. Create a session
    3. Get recent publications
    4. Display summaries
    5. Get and display detailed info for first publication
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

    load_dotenv()
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
    if not username or not password:
        logging.error("Please provide a username and password in the .env file.")
        return

    session = create_session(username, password)
    
    try:
        # Get recent publications
        publications = get_publications(session, size=5)
        
        if not publications:
            logging.warning("No publications found")
            return
        
        # Display summaries
        logging.info("\n" + "="*80)
        logging.info("RECENT PUBLICATIONS")
        logging.info("="*80)
        
        for pub in publications:
            display_publication_summary(pub)
        
        # Get detailed info for the first publication
        first_pub_id = int(publications[0]['publicatieId'])
        detailed_pub = get_publication_details(session, first_pub_id)
        
        display_detailed_publication(detailed_pub)
        
        logging.info("\n✓ Successfully retrieved publication data from TenderNed API")
        
    except Exception as e:
        logging.error(f"Failed: {e}")
        import traceback
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
