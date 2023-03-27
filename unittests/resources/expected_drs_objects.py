expected_good_drs_object = {
    "id": "697907bf-d5bd-433e-aac2-1747f1faf366",
    "description": "Phenopackets, Zhang family, 2009, proband",
    "created_time": "2021-03-12T20:00:00Z",
    "mime_type": "application/json",
    "name": "phenopackets.zhang.2009.proband",
    "size": 6471,
    "updated_time": "2021-03-13T12:30:45Z",
    "version": "1.0.0",
    "aliases": [
        "Zhang-EDA-proband"
    ],
    "checksums": [
        {
            "checksum": "b7e976ef2a9d13c65f154ad72a5495139dc6ac32",
            "type": "sha1"
        },
        {
            "checksum": "70722813447e98baf8f79cd5828668f971676bcfe08c286f62a7decd84b03eb0",
            "type": "sha256"
        },
        {
            "checksum": "71611ed3a3246fea6ce80916924c0722",
            "type": "md5"
        }
    ],
    "self_uri": "drs://localhost:4500/697907bf-d5bd-433e-aac2-1747f1faf366",
    "access_methods": [
        {
            "access_id": "338e433b-e0f4-4261-9d25-1863b2dcf08d",
            "type": "https"
        },
        {
            "access_url": {
                "url": "s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"
            },
            "type": "s3",
            "region": "us-east-2"
        }
    ]
}

expected_bad_drs_objects = [
    {
        "id": "697907bf-d5bd-433e-aac2-1747f1faf366",
        "description": "Phenopackets, Zhang family, 2009, proband",
        "created_time": "2021-03-12T20:00:00Z",
        "mime_type": "application/json",
        "name": "phenopackets.zhang.2009.proband",
        "size": 6471,
        "updated_time": "2021-03-13T12:30:45Z",
        "version": "1.0.0",
        "aliases": [
            "Zhang-EDA-proband"
        ],
        "self_uri": "drs://localhost:4500/697907bf-d5bd-433e-aac2-1747f1faf366",
        "access_methods": [
            {
                "access_id": "338e433b-e0f4-4261-9d25-1863b2dcf08d",
                "type": "https"
            },
            {
                "access_url": {
                    "url": "s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"
                },
                "type": "s3",
                "region": "us-east-2"
            }
        ]
    },
    {
        "description": "Phenopackets, Zhang family, 2009, proband",
        "created_time": "2021-03-12T20:00:00Z",
        "mime_type": "application/json",
        "name": "phenopackets.zhang.2009.proband",
        "size": 6471,
        "updated_time": "2021-03-13T12:30:45Z",
        "version": "1.0.0",
        "aliases": [
            "Zhang-EDA-proband"
        ],
        "checksums": [
            {
                "checksum": "b7e976ef2a9d13c65f154ad72a5495139dc6ac32",
                "type": "sha1"
            },
            {
                "checksum": "70722813447e98baf8f79cd5828668f971676bcfe08c286f62a7decd84b03eb0",
                "type": "sha256"
            },
            {
                "checksum": "71611ed3a3246fea6ce80916924c0722",
                "type": "md5"
            }
        ],
        "self_uri": "drs://localhost:4500/697907bf-d5bd-433e-aac2-1747f1faf366",
        "access_methods": [
            {
                "access_id": "338e433b-e0f4-4261-9d25-1863b2dcf08d",
                "type": "https"
            },
            {
                "access_url": {
                    "url": "s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"
                },
                "type": "s3",
                "region": "us-east-2"
            }
        ]
    },
    {
        "id": "697907bf-d5bd-433e-aac2-1747f1faf366",
        "description": "Phenopackets, Zhang family, 2009, proband",
        "created_time": "2021-03-12T20:00:00Z",
        "mime_type": "application/json",
        "name": "phenopackets.zhang.2009.proband",
        "updated_time": "2021-03-13T12:30:45Z",
        "version": "1.0.0",
        "aliases": [
            "Zhang-EDA-proband"
        ],
        "checksums": [
            {
                "checksum": "b7e976ef2a9d13c65f154ad72a5495139dc6ac32",
                "type": "sha1"
            },
            {
                "checksum": "70722813447e98baf8f79cd5828668f971676bcfe08c286f62a7decd84b03eb0",
                "type": "sha256"
            },
            {
                "checksum": "71611ed3a3246fea6ce80916924c0722",
                "type": "md5"
            }
        ],
        "self_uri": "drs://localhost:4500/697907bf-d5bd-433e-aac2-1747f1faf366",
        "access_methods": [
            {
                "access_id": "338e433b-e0f4-4261-9d25-1863b2dcf08d",
                "type": "https"
            },
            {
                "access_url": {
                    "url": "s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"
                },
                "type": "s3",
                "region": "us-east-2"
            }
        ]
    },
    {
        "id": "697907bf-d5bd-433e-aac2-1747f1faf366",
        "description": "Phenopackets, Zhang family, 2009, proband",
        "created_time": "2021-03-12T20:00:00Z",
        "mime_type": "application/json",
        "name": "phenopackets.zhang.2009.proband",
        "size": 6471,
        "updated_time": "2021-03-13T12:30:45Z",
        "version": "1.0.0",
        "aliases": [
            "Zhang-EDA-proband"
        ],
        "checksums": [
            {
                "checksum": "b7e976ef2a9d13c65f154ad72a5495139dc6ac32",
                "type": "sha1"
            },
            {
                "checksum": "70722813447e98baf8f79cd5828668f971676bcfe08c286f62a7decd84b03eb0",
                "type": "sha256"
            },
            {
                "checksum": "71611ed3a3246fea6ce80916924c0722",
                "type": "md5"
            }
        ],
        "access_methods": [
            {
                "access_id": "338e433b-e0f4-4261-9d25-1863b2dcf08d",
                "type": "https"
            },
            {
                "access_url": {
                    "url": "s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"
                },
                "type": "s3",
                "region": "us-east-2"
            }
        ]
    },
    {
        "id": "697907bf-d5bd-433e-aac2-1747f1faf366",
        "description": "Phenopackets, Zhang family, 2009, proband",
        "mime_type": "application/json",
        "name": "phenopackets.zhang.2009.proband",
        "size": 6471,
        "updated_time": "2021-03-13T12:30:45Z",
        "version": "1.0.0",
        "aliases": [
            "Zhang-EDA-proband"
        ],
        "checksums": [
            {
                "checksum": "b7e976ef2a9d13c65f154ad72a5495139dc6ac32",
                "type": "sha1"
            },
            {
                "checksum": "70722813447e98baf8f79cd5828668f971676bcfe08c286f62a7decd84b03eb0",
                "type": "sha256"
            },
            {
                "checksum": "71611ed3a3246fea6ce80916924c0722",
                "type": "md5"
            }
        ],
        "self_uri": "drs://localhost:4500/697907bf-d5bd-433e-aac2-1747f1faf366",
        "access_methods": [
            {
                "access_id": "338e433b-e0f4-4261-9d25-1863b2dcf08d",
                "type": "https"
            },
            {
                "access_url": {
                    "url": "s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"
                },
                "type": "s3",
                "region": "us-east-2"
            }
        ]
    }
]