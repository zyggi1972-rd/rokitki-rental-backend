<?php
return [
    'app' => [
        'name' => 'Rokitki',
        'base_url' => 'https://www.rokitki.com.pl',
        'env' => 'production',
        'timezone' => 'Europe/Warsaw'
    ],
    'db' => [
        'host' => 'localhost',
        'name' => 'rokitki',
        'user' => 'rokitki_user',
        'pass' => 'change_me',
        'charset' => 'utf8mb4'
    ],
    'security' => [
        'hash_key' => 'CHANGE_ME_RANDOM_32_CHARS',
        'csrf_key' => 'CHANGE_ME_RANDOM_32_CHARS'
    ],
    'mail' => [
        'from_email' => 'no-reply@rokitki.com.pl',
        'from_name' => 'Rokitki',
        'smtp_host' => '',
        'smtp_user' => '',
        'smtp_pass' => '',
        'smtp_port' => 587,
        'smtp_secure' => 'tls'
    ],
    'stripe' => [
        'secret_key' => 'sk_live_or_test',
        'publishable_key' => 'pk_live_or_test',
        'webhook_secret' => 'whsec_...'
    ],
    'oauth' => [
        'google' => [
            'client_id' => '',
            'client_secret' => '',
            'redirect_uri' => 'https://www.rokitki.com.pl/auth/google/callback'
        ],
        'facebook' => [
            'app_id' => '',
            'app_secret' => '',
            'redirect_uri' => 'https://www.rokitki.com.pl/auth/facebook/callback'
        ]
    ]
];

