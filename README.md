# TenderNed API voorbeeldcode

Alle aankondigingen op TenderNed zijn openbaar, zodat de gegevens voor iedereen beschikbaar zijn. Via de TenderNed API is het mogelijk om zowel historische als actuele aankondigingen op te halen.

## Aan de slag

### Lokale installatie

1. Zorg ervoor dat een recente versie van Python (3.11 of nieuwer) is geïnstalleerd. 
2. Met het volgende commando worden de vereisten geïnstalleerd: `pip install -r requirements.txt`
3. Kopieer `.env.dist` naar `.env` en vul de gegevens in. Heeft u nog geen inloggegevens? Deze kunt u aanvragen via [functioneelbeheer@tenderned.nl](mailto:functioneelbeheer@tenderned.nl)
4. Start het script via `python run.py` (gebruikt JSON API) of `python tenderned_json_api_example.py`

### Docker

U kunt de applicatie ook draaien met Docker:

```bash
# Zorg dat .env bestaat met je credentials
cp .env.dist .env
# Bewerk .env en vul je credentials in

# Run met docker-compose
docker-compose up --build

# Of direct met docker
docker build -t tenderned-api .
docker run --env-file .env tenderned-api
```

## Beschikbare scripts

### JSON API (Aanbevolen)
- **Bestand**: `tenderned_json_api_example.py`
- **Gebruik**: `python tenderned_json_api_example.py` of `python run.py --json`
- **Beschrijving**: Haalt publicaties op via de JSON API endpoint. Dit werkt voor alle recente publicaties.
- **Voordeel**: Altijd beschikbaar, volledige data structuur, eenvoudiger te parsen

### XML API (Beperkte beschikbaarheid)
- **Bestand**: `tenderned_xml_api_example.py`
- **Gebruik**: `python tenderned_xml_api_example.py` of `python run.py --xml`
- **Beschrijving**: Probeert publicaties op te halen via de XML export endpoint
- **Let op**: Niet alle publicaties hebben een XML export beschikbaar. Alleen oudere eForms publicaties ondersteunen dit.

### Runner script
- **Bestand**: `run.py`
- **Gebruik**: `python run.py [--json|--xml]`
- **Beschrijving**: Wrapper script om gemakkelijk tussen JSON en XML API te wisselen

## API endpoints

De TenderNed API biedt verschillende endpoints:

- `GET /publicaties` - Lijst van recente publicaties (JSON)
- `GET /publicaties/{id}` - Details van een specifieke publicatie (JSON)
- `GET /publicaties/{id}/public-xml` - XML export (beperkte beschikbaarheid)

Volledige documentatie: https://www.tenderned.nl/info/swagger

## Docker & GitHub Actions

Dit project bevat ook:

- **Dockerfile**: Voor containerisatie van de applicatie
- **docker-compose.yml**: Voor eenvoudig lokaal draaien
- **GitHub Actions workflows**: Geautomatiseerde CI/CD pipelines
  - `.github/workflows/ci.yml`: Linting, testing en Docker builds
  - `.github/workflows/docker-publish.yml`: Publiceer naar GitHub Container Registry
  - `.github/workflows/docker-compose-test.yml`: Test docker-compose setup

## Opmerkingen

1. De documentatie voor deze API is te vinden op https://www.tenderned.nl/info/swagger
2. Het XML voorbeeld werkt alleen met publicaties die een XML export hebben (voornamelijk oudere eForms)
3. Voor nieuwe projecten wordt de JSON API aanbevolen vanwege betere beschikbaarheid
4. Credentials worden nooit gecommit naar git (zie `.gitignore`)
