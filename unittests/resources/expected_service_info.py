expected_good_service_info_response = {
    "id": "org.ga4gh.starterkit.drs",
    "name": "GA4GH Starter Kit DRS Service",
    "description": "An open source, community-driven implementation of the GA4GH Data Repository Service (DRS) API specification.",
    "contactUrl": "mailto:info@ga4gh.org",
    "documentationUrl": "https://github.com/ga4gh/ga4gh-starter-kit-drs",
    "environment": "test",
    "version": "0.3.1",
    "type": {
        "group": "org.ga4gh",
        "artifact": "drs",
        "version": "1.2.0"
    },
    "organization": {
        "name": "Global Alliance for Genomics and Health",
        "url": "https://ga4gh.org"
    }
}

expected_bad_service_info_response = {
    "id": "org.ga4gh.starterkit.drs",
    "name": "GA4GH Starter Kit DRS Service",
    "description": "An open source, community-driven implementation of the GA4GH Data Repository Service (DRS) API specification.",
    "contactUrl": "mailto:info@ga4gh.org",
    "documentationUrl": "https://github.com/ga4gh/ga4gh-starter-kit-drs",
    "environment": "test",
    "version": "0.3.1",
    "organization": {
        "name": "Global Alliance for Genomics and Health",
    }
}
