"""Elasticsearch async client — locations index (cities, airports, states, countries)."""

import logging
from elasticsearch import AsyncElasticsearch, NotFoundError
from app.config import ELASTICSEARCH_URL, ELASTICSEARCH_LOCATIONS_INDEX

logger = logging.getLogger(__name__)

_es_client: AsyncElasticsearch | None = None


def get_es_client() -> AsyncElasticsearch:
    global _es_client
    if _es_client is None:
        _es_client = AsyncElasticsearch(
            hosts=[ELASTICSEARCH_URL],
            retry_on_timeout=True,
            max_retries=3,
        )
    return _es_client


async def close_es():
    global _es_client
    if _es_client:
        await _es_client.close()
        _es_client = None


# ─── Index mapping ────────────────────────────────────────────────────────────

INDEX_MAPPING = {
    "settings": {
        "analysis": {
            "analyzer": {
                "location_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"],
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name":        {"type": "text",    "analyzer": "location_analyzer", "fields": {"keyword": {"type": "keyword"}}},
            "code":        {"type": "keyword"},
            "type":        {"type": "keyword"},
            "country":     {"type": "text",    "analyzer": "location_analyzer", "fields": {"keyword": {"type": "keyword"}}},
            "state":       {"type": "text",    "analyzer": "location_analyzer"},
            "description": {"type": "text",    "analyzer": "location_analyzer"},
            "aliases":     {"type": "text",    "analyzer": "location_analyzer"},
        }
    },
}

# ─── Seed data ────────────────────────────────────────────────────────────────

LOCATIONS_SEED = [
    # ── Indian cities / airports ──────────────────────────────────────────────
    {"id": "DEL", "name": "New Delhi", "code": "DEL", "type": "city", "country": "India", "state": "Delhi", "description": "Indira Gandhi International Airport", "aliases": "Delhi IGI"},
    {"id": "BOM", "name": "Mumbai", "code": "BOM", "type": "city", "country": "India", "state": "Maharashtra", "description": "Chhatrapati Shivaji Maharaj International Airport", "aliases": "Bombay CSIA"},
    {"id": "BLR", "name": "Bangalore", "code": "BLR", "type": "city", "country": "India", "state": "Karnataka", "description": "Kempegowda International Airport", "aliases": "Bengaluru KIA"},
    {"id": "MAA", "name": "Chennai", "code": "MAA", "type": "city", "country": "India", "state": "Tamil Nadu", "description": "Chennai International Airport", "aliases": "Madras"},
    {"id": "CCU", "name": "Kolkata", "code": "CCU", "type": "city", "country": "India", "state": "West Bengal", "description": "Netaji Subhas Chandra Bose International Airport", "aliases": "Calcutta NSCBI"},
    {"id": "HYD", "name": "Hyderabad", "code": "HYD", "type": "city", "country": "India", "state": "Telangana", "description": "Rajiv Gandhi International Airport", "aliases": "Cyberabad RGIA"},
    {"id": "GOI", "name": "Goa", "code": "GOI", "type": "city", "country": "India", "state": "Goa", "description": "Goa International Airport (Dabolim)", "aliases": "Panaji Dabolim"},
    {"id": "JAI", "name": "Jaipur", "code": "JAI", "type": "city", "country": "India", "state": "Rajasthan", "description": "Jaipur International Airport", "aliases": "Pink City"},
    {"id": "AMD", "name": "Ahmedabad", "code": "AMD", "type": "city", "country": "India", "state": "Gujarat", "description": "Sardar Vallabhbhai Patel International Airport", "aliases": "Amdavad SVPIA"},
    {"id": "PNQ", "name": "Pune", "code": "PNQ", "type": "city", "country": "India", "state": "Maharashtra", "description": "Pune Airport", "aliases": "Poona"},
    {"id": "COK", "name": "Kochi", "code": "COK", "type": "city", "country": "India", "state": "Kerala", "description": "Cochin International Airport", "aliases": "Cochin CIAL"},
    {"id": "TRV", "name": "Thiruvananthapuram", "code": "TRV", "type": "city", "country": "India", "state": "Kerala", "description": "Trivandrum International Airport", "aliases": "Trivandrum"},
    {"id": "IXC", "name": "Chandigarh", "code": "IXC", "type": "city", "country": "India", "state": "Punjab", "description": "Chandigarh International Airport", "aliases": ""},
    {"id": "LKO", "name": "Lucknow", "code": "LKO", "type": "city", "country": "India", "state": "Uttar Pradesh", "description": "Chaudhary Charan Singh International Airport", "aliases": "Nawabi"},
    {"id": "BBI", "name": "Bhubaneswar", "code": "BBI", "type": "city", "country": "India", "state": "Odisha", "description": "Biju Patnaik International Airport", "aliases": "Bhubhaneshwar"},
    {"id": "GAU", "name": "Guwahati", "code": "GAU", "type": "city", "country": "India", "state": "Assam", "description": "Lokpriya Gopinath Bordoloi International Airport", "aliases": "Gauhati"},
    {"id": "NAG", "name": "Nagpur", "code": "NAG", "type": "city", "country": "India", "state": "Maharashtra", "description": "Dr. Babasaheb Ambedkar International Airport", "aliases": "Orange City"},
    {"id": "VTZ", "name": "Visakhapatnam", "code": "VTZ", "type": "city", "country": "India", "state": "Andhra Pradesh", "description": "Visakhapatnam Airport", "aliases": "Vizag"},
    {"id": "IXZ", "name": "Port Blair", "code": "IXZ", "type": "city", "country": "India", "state": "Andaman and Nicobar Islands", "description": "Veer Savarkar International Airport", "aliases": "Andaman"},
    {"id": "SXR", "name": "Srinagar", "code": "SXR", "type": "city", "country": "India", "state": "Jammu and Kashmir", "description": "Sheikh ul-Alam International Airport", "aliases": "Kashmir"},
    {"id": "IMF", "name": "Imphal", "code": "IMF", "type": "city", "country": "India", "state": "Manipur", "description": "Bir Tikendrajit International Airport", "aliases": ""},
    {"id": "IXB", "name": "Bagdogra", "code": "IXB", "type": "city", "country": "India", "state": "West Bengal", "description": "Bagdogra Airport (serves Darjeeling & Sikkim)", "aliases": "Siliguri Darjeeling"},
    {"id": "UDR", "name": "Udaipur", "code": "UDR", "type": "city", "country": "India", "state": "Rajasthan", "description": "Maharana Pratap Airport", "aliases": "City of Lakes"},
    {"id": "IXJ", "name": "Jammu", "code": "IXJ", "type": "city", "country": "India", "state": "Jammu and Kashmir", "description": "Jammu Airport (Satwari)", "aliases": ""},
    {"id": "RPR", "name": "Raipur", "code": "RPR", "type": "city", "country": "India", "state": "Chhattisgarh", "description": "Swami Vivekananda Airport", "aliases": ""},
    {"id": "BHO", "name": "Bhopal", "code": "BHO", "type": "city", "country": "India", "state": "Madhya Pradesh", "description": "Raja Bhoj Airport", "aliases": ""},
    {"id": "IDR", "name": "Indore", "code": "IDR", "type": "city", "country": "India", "state": "Madhya Pradesh", "description": "Devi Ahilya Bai Holkar Airport", "aliases": ""},
    {"id": "VNS", "name": "Varanasi", "code": "VNS", "type": "city", "country": "India", "state": "Uttar Pradesh", "description": "Lal Bahadur Shastri International Airport", "aliases": "Banaras Benares Kashi"},
    {"id": "ATQ", "name": "Amritsar", "code": "ATQ", "type": "city", "country": "India", "state": "Punjab", "description": "Sri Guru Ram Dass Jee International Airport", "aliases": "Golden Temple"},
    {"id": "IXR", "name": "Ranchi", "code": "IXR", "type": "city", "country": "India", "state": "Jharkhand", "description": "Birsa Munda Airport", "aliases": ""},

    # ── Indian states ─────────────────────────────────────────────────────────
    {"id": "IN-DL",  "name": "Delhi",                       "code": "DL",  "type": "state", "country": "India", "state": "Delhi",                       "description": "National Capital Territory of India", "aliases": "New Delhi NCT"},
    {"id": "IN-MH",  "name": "Maharashtra",                 "code": "MH",  "type": "state", "country": "India", "state": "Maharashtra",                 "description": "State — Mumbai, Pune, Nagpur", "aliases": "Mumbai state"},
    {"id": "IN-KA",  "name": "Karnataka",                   "code": "KA",  "type": "state", "country": "India", "state": "Karnataka",                   "description": "State — Bangalore, Mysuru, Hubli", "aliases": "Bengaluru state"},
    {"id": "IN-TN",  "name": "Tamil Nadu",                  "code": "TN",  "type": "state", "country": "India", "state": "Tamil Nadu",                  "description": "State — Chennai, Coimbatore, Madurai", "aliases": "Madras state"},
    {"id": "IN-WB",  "name": "West Bengal",                 "code": "WB",  "type": "state", "country": "India", "state": "West Bengal",                 "description": "State — Kolkata, Darjeeling, Siliguri", "aliases": "Bengal Calcutta"},
    {"id": "IN-TS",  "name": "Telangana",                   "code": "TS",  "type": "state", "country": "India", "state": "Telangana",                   "description": "State — Hyderabad, Warangal", "aliases": "Hyderabad state"},
    {"id": "IN-GA",  "name": "Goa",                         "code": "GA",  "type": "state", "country": "India", "state": "Goa",                         "description": "State — Panaji, Margao, Vasco da Gama", "aliases": "Beach state"},
    {"id": "IN-RJ",  "name": "Rajasthan",                   "code": "RJ",  "type": "state", "country": "India", "state": "Rajasthan",                   "description": "State — Jaipur, Udaipur, Jodhpur, Jaisalmer", "aliases": "Desert state Pink City"},
    {"id": "IN-GJ",  "name": "Gujarat",                     "code": "GJ",  "type": "state", "country": "India", "state": "Gujarat",                     "description": "State — Ahmedabad, Surat, Vadodara", "aliases": ""},
    {"id": "IN-KL",  "name": "Kerala",                      "code": "KL",  "type": "state", "country": "India", "state": "Kerala",                      "description": "State — Kochi, Thiruvananthapuram, Kozhikode", "aliases": "God's Own Country backwaters"},
    {"id": "IN-UP",  "name": "Uttar Pradesh",               "code": "UP",  "type": "state", "country": "India", "state": "Uttar Pradesh",               "description": "State — Lucknow, Varanasi, Agra, Kanpur", "aliases": "UP"},
    {"id": "IN-PB",  "name": "Punjab",                      "code": "PB",  "type": "state", "country": "India", "state": "Punjab",                      "description": "State — Amritsar, Chandigarh, Ludhiana", "aliases": "Land of five rivers"},
    {"id": "IN-AP",  "name": "Andhra Pradesh",              "code": "AP",  "type": "state", "country": "India", "state": "Andhra Pradesh",              "description": "State — Visakhapatnam, Vijayawada, Tirupati", "aliases": ""},
    {"id": "IN-OR",  "name": "Odisha",                      "code": "OR",  "type": "state", "country": "India", "state": "Odisha",                      "description": "State — Bhubaneswar, Puri, Cuttack", "aliases": "Orissa"},
    {"id": "IN-AS",  "name": "Assam",                       "code": "AS",  "type": "state", "country": "India", "state": "Assam",                       "description": "State — Guwahati, Jorhat, Dibrugarh", "aliases": "Northeast India tea"},
    {"id": "IN-BR",  "name": "Bihar",                       "code": "BR",  "type": "state", "country": "India", "state": "Bihar",                       "description": "State — Patna, Gaya, Bodh Gaya", "aliases": ""},
    {"id": "IN-MP",  "name": "Madhya Pradesh",              "code": "MP",  "type": "state", "country": "India", "state": "Madhya Pradesh",              "description": "State — Bhopal, Indore, Gwalior, Ujjain", "aliases": "Heart of India"},
    {"id": "IN-CG",  "name": "Chhattisgarh",                "code": "CG",  "type": "state", "country": "India", "state": "Chhattisgarh",                "description": "State — Raipur, Bilaspur", "aliases": ""},
    {"id": "IN-JH",  "name": "Jharkhand",                   "code": "JH",  "type": "state", "country": "India", "state": "Jharkhand",                   "description": "State — Ranchi, Jamshedpur, Dhanbad", "aliases": ""},
    {"id": "IN-HP",  "name": "Himachal Pradesh",            "code": "HP",  "type": "state", "country": "India", "state": "Himachal Pradesh",            "description": "State — Shimla, Manali, Dharamshala", "aliases": "Hill station mountains"},
    {"id": "IN-UK",  "name": "Uttarakhand",                 "code": "UK",  "type": "state", "country": "India", "state": "Uttarakhand",                 "description": "State — Dehradun, Haridwar, Rishikesh, Nainital", "aliases": "Uttaranchal"},
    {"id": "IN-JK",  "name": "Jammu and Kashmir",           "code": "JK",  "type": "state", "country": "India", "state": "Jammu and Kashmir",           "description": "UT — Srinagar, Jammu, Leh", "aliases": "Kashmir J&K"},
    {"id": "IN-LA",  "name": "Ladakh",                      "code": "LA",  "type": "state", "country": "India", "state": "Ladakh",                      "description": "UT — Leh, Kargil", "aliases": "Land of high passes"},
    {"id": "IN-MN",  "name": "Manipur",                     "code": "MN",  "type": "state", "country": "India", "state": "Manipur",                     "description": "State — Imphal", "aliases": "Northeast"},
    {"id": "IN-SK",  "name": "Sikkim",                      "code": "SK",  "type": "state", "country": "India", "state": "Sikkim",                      "description": "State — Gangtok", "aliases": "Northeast Himalayan"},

    # ── International cities / airports ───────────────────────────────────────
    {"id": "DXB", "name": "Dubai",           "code": "DXB", "type": "city", "country": "United Arab Emirates", "state": "Dubai",              "description": "Dubai International Airport",                "aliases": "UAE Emirates"},
    {"id": "LHR", "name": "London",          "code": "LHR", "type": "city", "country": "United Kingdom",       "state": "England",            "description": "Heathrow Airport",                           "aliases": "Heathrow UK Britain"},
    {"id": "JFK", "name": "New York",        "code": "JFK", "type": "city", "country": "United States",        "state": "New York",           "description": "John F. Kennedy International Airport",      "aliases": "NYC Manhattan USA America"},
    {"id": "SIN", "name": "Singapore",       "code": "SIN", "type": "city", "country": "Singapore",            "state": "",                   "description": "Changi Airport",                             "aliases": "Changi SG Lion City"},
    {"id": "BKK", "name": "Bangkok",         "code": "BKK", "type": "city", "country": "Thailand",             "state": "",                   "description": "Suvarnabhumi Airport",                       "aliases": "Suvarnabhumi Thailand"},
    {"id": "CDG", "name": "Paris",           "code": "CDG", "type": "city", "country": "France",               "state": "Île-de-France",      "description": "Charles de Gaulle Airport",                  "aliases": "France Eiffel CDG"},
    {"id": "SYD", "name": "Sydney",          "code": "SYD", "type": "city", "country": "Australia",            "state": "New South Wales",    "description": "Sydney Kingsford Smith Airport",             "aliases": "Kingsford Smith Australia"},
    {"id": "NRT", "name": "Tokyo",           "code": "NRT", "type": "city", "country": "Japan",                "state": "Tokyo",              "description": "Narita International Airport",               "aliases": "Japan Narita"},
    {"id": "YYZ", "name": "Toronto",         "code": "YYZ", "type": "city", "country": "Canada",               "state": "Ontario",            "description": "Toronto Pearson International Airport",      "aliases": "Pearson Canada"},
    {"id": "KUL", "name": "Kuala Lumpur",    "code": "KUL", "type": "city", "country": "Malaysia",             "state": "",                   "description": "Kuala Lumpur International Airport (KLIA)",  "aliases": "KLIA Malaysia KL"},
    {"id": "FRA", "name": "Frankfurt",       "code": "FRA", "type": "city", "country": "Germany",              "state": "Hesse",              "description": "Frankfurt Airport",                          "aliases": "Germany FRA"},
    {"id": "AMS", "name": "Amsterdam",       "code": "AMS", "type": "city", "country": "Netherlands",          "state": "North Holland",      "description": "Amsterdam Schiphol Airport",                 "aliases": "Schiphol Holland"},
    {"id": "DOH", "name": "Doha",            "code": "DOH", "type": "city", "country": "Qatar",                "state": "",                   "description": "Hamad International Airport",                "aliases": "Qatar Hamad"},
    {"id": "ICN", "name": "Seoul",           "code": "ICN", "type": "city", "country": "South Korea",          "state": "",                   "description": "Incheon International Airport",              "aliases": "Korea Incheon"},
    {"id": "HKG", "name": "Hong Kong",       "code": "HKG", "type": "city", "country": "Hong Kong",            "state": "",                   "description": "Hong Kong International Airport",            "aliases": "HK Chek Lap Kok"},
    {"id": "MEL", "name": "Melbourne",       "code": "MEL", "type": "city", "country": "Australia",            "state": "Victoria",           "description": "Melbourne Airport",                          "aliases": "Tullamarine Australia"},
    {"id": "LAX", "name": "Los Angeles",     "code": "LAX", "type": "city", "country": "United States",        "state": "California",         "description": "Los Angeles International Airport",          "aliases": "LA Hollywood USA"},
    {"id": "ORD", "name": "Chicago",         "code": "ORD", "type": "city", "country": "United States",        "state": "Illinois",           "description": "O'Hare International Airport",               "aliases": "O'Hare USA"},
    {"id": "PEK", "name": "Beijing",         "code": "PEK", "type": "city", "country": "China",                "state": "Beijing",            "description": "Beijing Capital International Airport",      "aliases": "China Capital"},
    {"id": "PVG", "name": "Shanghai",        "code": "PVG", "type": "city", "country": "China",                "state": "Shanghai",           "description": "Shanghai Pudong International Airport",      "aliases": "China Pudong"},
    {"id": "IST", "name": "Istanbul",        "code": "IST", "type": "city", "country": "Turkey",               "state": "",                   "description": "Istanbul Airport",                           "aliases": "Turkey Constantinople"},
    {"id": "ZRH", "name": "Zurich",          "code": "ZRH", "type": "city", "country": "Switzerland",          "state": "",                   "description": "Zurich Airport",                             "aliases": "Switzerland"},
    {"id": "MNL", "name": "Manila",          "code": "MNL", "type": "city", "country": "Philippines",          "state": "",                   "description": "Ninoy Aquino International Airport",         "aliases": "Philippines NAIA"},
    {"id": "CGK", "name": "Jakarta",         "code": "CGK", "type": "city", "country": "Indonesia",            "state": "DKI Jakarta",        "description": "Soekarno-Hatta International Airport",       "aliases": "Indonesia Soetta"},
    {"id": "JNB", "name": "Johannesburg",    "code": "JNB", "type": "city", "country": "South Africa",         "state": "Gauteng",            "description": "O.R. Tambo International Airport",           "aliases": "OR Tambo South Africa JHB"},
    {"id": "CAI", "name": "Cairo",           "code": "CAI", "type": "city", "country": "Egypt",                "state": "",                   "description": "Cairo International Airport",                "aliases": "Egypt Pyramid"},
    {"id": "GRU", "name": "São Paulo",       "code": "GRU", "type": "city", "country": "Brazil",               "state": "São Paulo",          "description": "São Paulo/Guarulhos–Governador André Franco Montoro International Airport", "aliases": "Sao Paulo Brazil"},
    {"id": "MEX", "name": "Mexico City",     "code": "MEX", "type": "city", "country": "Mexico",               "state": "Mexico City",        "description": "Benito Juárez International Airport",        "aliases": "Mexico CDMX"},
    {"id": "AKL", "name": "Auckland",        "code": "AKL", "type": "city", "country": "New Zealand",          "state": "",                   "description": "Auckland Airport",                           "aliases": "NZ New Zealand"},
    {"id": "VIE", "name": "Vienna",          "code": "VIE", "type": "city", "country": "Austria",              "state": "",                   "description": "Vienna International Airport",               "aliases": "Austria"},
    {"id": "BCN", "name": "Barcelona",       "code": "BCN", "type": "city", "country": "Spain",                "state": "Catalonia",          "description": "Barcelona–El Prat Airport",                  "aliases": "Spain Catalonia"},
    {"id": "MAD", "name": "Madrid",          "code": "MAD", "type": "city", "country": "Spain",                "state": "Community of Madrid","description": "Adolfo Suárez Madrid–Barajas Airport",        "aliases": "Spain"},
    {"id": "FCO", "name": "Rome",            "code": "FCO", "type": "city", "country": "Italy",                "state": "Lazio",              "description": "Leonardo da Vinci International Airport",    "aliases": "Italy Fiumicino"},
    {"id": "MXP", "name": "Milan",           "code": "MXP", "type": "city", "country": "Italy",                "state": "Lombardy",           "description": "Milan Malpensa Airport",                     "aliases": "Italy Malpensa"},
    {"id": "DME", "name": "Moscow",          "code": "DME", "type": "city", "country": "Russia",               "state": "Moscow Oblast",      "description": "Domodedovo International Airport",           "aliases": "Russia Domodedovo"},
    {"id": "CPT", "name": "Cape Town",       "code": "CPT", "type": "city", "country": "South Africa",         "state": "Western Cape",       "description": "Cape Town International Airport",            "aliases": "South Africa"},
    {"id": "LOS", "name": "Lagos",           "code": "LOS", "type": "city", "country": "Nigeria",              "state": "Lagos",              "description": "Murtala Muhammed International Airport",     "aliases": "Nigeria"},
    {"id": "ADD", "name": "Addis Ababa",     "code": "ADD", "type": "city", "country": "Ethiopia",             "state": "",                   "description": "Addis Ababa Bole International Airport",     "aliases": "Ethiopia Bole"},
    {"id": "NBO", "name": "Nairobi",         "code": "NBO", "type": "city", "country": "Kenya",                "state": "",                   "description": "Jomo Kenyatta International Airport",        "aliases": "Kenya JKIA"},
    {"id": "CMB", "name": "Colombo",         "code": "CMB", "type": "city", "country": "Sri Lanka",            "state": "",                   "description": "Bandaranaike International Airport",         "aliases": "Sri Lanka Lanka"},
    {"id": "DAC", "name": "Dhaka",           "code": "DAC", "type": "city", "country": "Bangladesh",           "state": "Dhaka",              "description": "Hazrat Shahjalal International Airport",     "aliases": "Bangladesh"},
    {"id": "KTM", "name": "Kathmandu",       "code": "KTM", "type": "city", "country": "Nepal",                "state": "Bagmati",            "description": "Tribhuvan International Airport",            "aliases": "Nepal Himalaya"},

    # ── Countries ─────────────────────────────────────────────────────────────
    {"id": "COUNTRY-IN",  "name": "India",               "code": "IN",  "type": "country", "country": "India",                "state": "", "description": "Republic of India — 28 states, 8 UTs", "aliases": "Bharat Hindustan"},
    {"id": "COUNTRY-US",  "name": "United States",       "code": "US",  "type": "country", "country": "United States",        "state": "", "description": "United States of America", "aliases": "USA America"},
    {"id": "COUNTRY-GB",  "name": "United Kingdom",      "code": "GB",  "type": "country", "country": "United Kingdom",       "state": "", "description": "England, Scotland, Wales, Northern Ireland", "aliases": "UK Britain"},
    {"id": "COUNTRY-AE",  "name": "United Arab Emirates","code": "AE",  "type": "country", "country": "United Arab Emirates", "state": "", "description": "UAE — Dubai, Abu Dhabi, Sharjah", "aliases": "UAE Emirates Gulf"},
    {"id": "COUNTRY-SG",  "name": "Singapore",           "code": "SG",  "type": "country", "country": "Singapore",            "state": "", "description": "Republic of Singapore", "aliases": "Lion City SG"},
    {"id": "COUNTRY-TH",  "name": "Thailand",            "code": "TH",  "type": "country", "country": "Thailand",             "state": "", "description": "Kingdom of Thailand — Bangkok, Phuket, Chiang Mai", "aliases": ""},
    {"id": "COUNTRY-FR",  "name": "France",              "code": "FR",  "type": "country", "country": "France",               "state": "", "description": "French Republic — Paris, Lyon, Marseille", "aliases": ""},
    {"id": "COUNTRY-AU",  "name": "Australia",           "code": "AU",  "type": "country", "country": "Australia",            "state": "", "description": "Commonwealth of Australia", "aliases": "OZ Down Under"},
    {"id": "COUNTRY-JP",  "name": "Japan",               "code": "JP",  "type": "country", "country": "Japan",                "state": "", "description": "Japan — Tokyo, Osaka, Kyoto", "aliases": "Nihon Nippon"},
    {"id": "COUNTRY-CA",  "name": "Canada",              "code": "CA",  "type": "country", "country": "Canada",               "state": "", "description": "Canada — Toronto, Vancouver, Montreal", "aliases": ""},
    {"id": "COUNTRY-MY",  "name": "Malaysia",            "code": "MY",  "type": "country", "country": "Malaysia",             "state": "", "description": "Malaysia — Kuala Lumpur, Penang, Langkawi", "aliases": ""},
    {"id": "COUNTRY-DE",  "name": "Germany",             "code": "DE",  "type": "country", "country": "Germany",              "state": "", "description": "Germany — Berlin, Frankfurt, Munich", "aliases": "Deutschland"},
    {"id": "COUNTRY-QA",  "name": "Qatar",               "code": "QA",  "type": "country", "country": "Qatar",                "state": "", "description": "Qatar — Doha", "aliases": ""},
    {"id": "COUNTRY-KR",  "name": "South Korea",         "code": "KR",  "type": "country", "country": "South Korea",          "state": "", "description": "Republic of Korea — Seoul, Busan", "aliases": "Korea"},
    {"id": "COUNTRY-HK",  "name": "Hong Kong",           "code": "HK",  "type": "country", "country": "Hong Kong",            "state": "", "description": "Hong Kong SAR", "aliases": ""},
    {"id": "COUNTRY-NL",  "name": "Netherlands",         "code": "NL",  "type": "country", "country": "Netherlands",          "state": "", "description": "Netherlands — Amsterdam, Rotterdam", "aliases": "Holland Dutch"},
    {"id": "COUNTRY-NZ",  "name": "New Zealand",         "code": "NZ",  "type": "country", "country": "New Zealand",          "state": "", "description": "New Zealand — Auckland, Wellington, Queenstown", "aliases": "NZ Kiwi"},
    {"id": "COUNTRY-ZA",  "name": "South Africa",        "code": "ZA",  "type": "country", "country": "South Africa",         "state": "", "description": "South Africa — Cape Town, Johannesburg", "aliases": ""},
    {"id": "COUNTRY-ID",  "name": "Indonesia",           "code": "ID",  "type": "country", "country": "Indonesia",            "state": "", "description": "Indonesia — Bali, Jakarta, Yogyakarta", "aliases": "Bali"},
    {"id": "COUNTRY-LK",  "name": "Sri Lanka",           "code": "LK",  "type": "country", "country": "Sri Lanka",            "state": "", "description": "Sri Lanka — Colombo, Kandy, Galle", "aliases": "Lanka Ceylon"},
    {"id": "COUNTRY-NP",  "name": "Nepal",               "code": "NP",  "type": "country", "country": "Nepal",                "state": "", "description": "Nepal — Kathmandu, Pokhara, Chitwan", "aliases": "Himalaya"},
    {"id": "COUNTRY-BD",  "name": "Bangladesh",          "code": "BD",  "type": "country", "country": "Bangladesh",           "state": "", "description": "Bangladesh — Dhaka, Chittagong", "aliases": ""},
    {"id": "COUNTRY-IT",  "name": "Italy",               "code": "IT",  "type": "country", "country": "Italy",                "state": "", "description": "Italy — Rome, Milan, Venice, Florence", "aliases": "Italia"},
    {"id": "COUNTRY-ES",  "name": "Spain",               "code": "ES",  "type": "country", "country": "Spain",                "state": "", "description": "Spain — Madrid, Barcelona, Seville", "aliases": "Espana"},
    {"id": "COUNTRY-TR",  "name": "Turkey",              "code": "TR",  "type": "country", "country": "Turkey",               "state": "", "description": "Turkey — Istanbul, Ankara, Antalya", "aliases": "Türkiye"},
    {"id": "COUNTRY-EG",  "name": "Egypt",               "code": "EG",  "type": "country", "country": "Egypt",                "state": "", "description": "Egypt — Cairo, Luxor, Sharm el-Sheikh", "aliases": "Pyramid"},
    {"id": "COUNTRY-KE",  "name": "Kenya",               "code": "KE",  "type": "country", "country": "Kenya",                "state": "", "description": "Kenya — Nairobi, Mombasa, Maasai Mara", "aliases": "Safari"},
    {"id": "COUNTRY-NG",  "name": "Nigeria",             "code": "NG",  "type": "country", "country": "Nigeria",              "state": "", "description": "Nigeria — Lagos, Abuja", "aliases": ""},
    {"id": "COUNTRY-ET",  "name": "Ethiopia",            "code": "ET",  "type": "country", "country": "Ethiopia",             "state": "", "description": "Ethiopia — Addis Ababa", "aliases": ""},
    {"id": "COUNTRY-BR",  "name": "Brazil",              "code": "BR",  "type": "country", "country": "Brazil",               "state": "", "description": "Brazil — São Paulo, Rio de Janeiro", "aliases": "Brasil"},
    {"id": "COUNTRY-MX",  "name": "Mexico",              "code": "MX",  "type": "country", "country": "Mexico",               "state": "", "description": "Mexico — Mexico City, Cancun", "aliases": ""},
    {"id": "COUNTRY-PH",  "name": "Philippines",         "code": "PH",  "type": "country", "country": "Philippines",          "state": "", "description": "Philippines — Manila, Cebu, Davao", "aliases": ""},
    {"id": "COUNTRY-CH",  "name": "Switzerland",         "code": "CH",  "type": "country", "country": "Switzerland",          "state": "", "description": "Switzerland — Zurich, Geneva, Bern", "aliases": "Swiss"},
    {"id": "COUNTRY-AT",  "name": "Austria",             "code": "AT",  "type": "country", "country": "Austria",              "state": "", "description": "Austria — Vienna, Salzburg, Innsbruck", "aliases": ""},
    {"id": "COUNTRY-CN",  "name": "China",               "code": "CN",  "type": "country", "country": "China",                "state": "", "description": "China — Beijing, Shanghai, Guangzhou", "aliases": "PRC"},
    {"id": "COUNTRY-RU",  "name": "Russia",              "code": "RU",  "type": "country", "country": "Russia",               "state": "", "description": "Russia — Moscow, Saint Petersburg", "aliases": ""},
]


# ─── Seed / re-index ─────────────────────────────────────────────────────────

async def ensure_index_and_seed():
    """Create the locations index if needed and bulk-index all seed data."""
    es = get_es_client()
    try:
        exists = await es.indices.exists(index=ELASTICSEARCH_LOCATIONS_INDEX)
        if not exists:
            await es.indices.create(index=ELASTICSEARCH_LOCATIONS_INDEX, body=INDEX_MAPPING)
            logger.info("Created Elasticsearch index '%s'", ELASTICSEARCH_LOCATIONS_INDEX)

        count_resp = await es.count(index=ELASTICSEARCH_LOCATIONS_INDEX)
        if count_resp["count"] == 0:
            logger.info("Seeding %d locations into Elasticsearch…", len(LOCATIONS_SEED))
            ops = []
            for doc in LOCATIONS_SEED:
                ops.append({"index": {"_index": ELASTICSEARCH_LOCATIONS_INDEX, "_id": doc["id"]}})
                ops.append({k: v for k, v in doc.items() if k != "id"})
            await es.bulk(operations=ops, refresh=True)
            logger.info("Elasticsearch seed complete.")
        else:
            logger.info("Elasticsearch index '%s' already has data (%d docs) — skipping seed.",
                        ELASTICSEARCH_LOCATIONS_INDEX, count_resp["count"])
    except Exception as exc:
        logger.warning("Elasticsearch seed skipped — %s: %s", type(exc).__name__, exc)


# ─── Search helper ─────────────────────────────────────────────────────────

async def search_locations(query: str, location_type: str | None = None, size: int = 8) -> list[dict]:
    """
    Search the locations index using a combined strategy:
      1. phrase_prefix  — handles prefix typing ("mum" → Mumbai, "del" → Delhi)
      2. fuzzy          — handles typos ("bangalor" → Bangalore)
      3. code exact     — instant IATA code match ("BOM", "DEL")
    Results are deduplicated and ranked by best score.
    """
    es = get_es_client()

    q = query.strip()
    filter_clauses = []
    if location_type:
        filter_clauses.append({"term": {"type": location_type}})

    body = {
        "query": {
            "bool": {
                "should": [
                    # ── 1. Prefix match on name (highest boost — handles live typing) ──
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["name^5", "aliases^3", "state^2", "country^2", "description"],
                            "type": "phrase_prefix",
                            "max_expansions": 50,
                        }
                    },
                    # ── 2. Fuzzy match — handles typos ──────────────────────────────
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["name^4", "aliases^2", "state", "country", "description"],
                            "type": "best_fields",
                            "fuzziness": "AUTO",
                            "prefix_length": 1,
                        }
                    },
                    # ── 3. Exact IATA / ISO code match (highest priority) ────────────
                    {
                        "term": {
                            "code": {"value": q.upper(), "boost": 10}
                        }
                    },
                ],
                "filter": filter_clauses,
                "minimum_should_match": 1,
            }
        },
        "size": size,
    }

    try:
        resp = await es.search(index=ELASTICSEARCH_LOCATIONS_INDEX, body=body)
        hits = resp["hits"]["hits"]
        return [{"id": h["_id"], **h["_source"], "score": round(h["_score"], 3)} for h in hits]
    except Exception as exc:
        logger.error("Elasticsearch search failed: %s", exc)
        return []
