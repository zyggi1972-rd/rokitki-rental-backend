<?php
$appName = $baseUrl ? 'Rokitki' : 'Rokitki';
?><!doctype html>
<html lang="pl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= htmlspecialchars($appName) ?></title>
    <link rel="icon" href="/assets/favicon.ico">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/assets/styles.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
        <div class="container">
            <a class="navbar-brand fw-bold text-primary" href="/">Rokitki</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="nav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item"><a class="nav-link" href="/blog">Blog</a></li>
                    <li class="nav-item"><a class="nav-link" href="/offers">Oferty</a></li>
                </ul>
                <div class="d-flex gap-2">
                    <?php if (!empty($_SESSION['user_id'])): ?>
                        <a class="btn btn-outline-primary" href="/dashboard">Panel</a>
                        <a class="btn btn-primary" href="/offers/new">Dodaj ogłoszenie</a>
                        <a class="btn btn-link" href="/logout">Wyloguj</a>
                    <?php else: ?>
                        <a class="btn btn-primary" href="/login">Zaloguj</a>
                        <a class="btn btn-outline-secondary" href="/register">Rejestracja</a>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </nav>
    <main class="py-4">
        <div class="container">
            <?= $content ?>
        </div>
    </main>
    <footer class="bg-light border-top py-4 mt-5">
        <div class="container small">
            <div class="row g-3">
                <div class="col-md-3">
                    <div class="fw-bold mb-2">Rokitki</div>
                    <div>Domki nad jeziorem · Lato i słońce</div>
                </div>
                <div class="col-md-3">
                    <div class="fw-bold mb-2">Informacje</div>
                    <ul class="list-unstyled">
                        <li><a href="/how-it-works">Jak to działa</a></li>
                        <li><a href="/why-us">Dlaczego Rokitki</a></li>
                        <li><a href="/about">O nas</a></li>
                        <li><a href="/faq">FAQ</a></li>
                    </ul>
                </div>
                <div class="col-md-3">
                    <div class="fw-bold mb-2">Regulaminy</div>
                    <ul class="list-unstyled">
                        <li><a href="/terms">Regulamin</a></li>
                        <li><a href="/privacy">Polityka prywatności</a></li>
                        <li><a href="/cookies">Polityka cookies</a></li>
                    </ul>
                </div>
                <div class="col-md-3">
                    <div class="fw-bold mb-2">Newsletter</div>
                    <form method="post" action="/newsletter/subscribe" class="d-flex gap-2">
                        <input type="email" class="form-control" name="email" placeholder="Twój e-mail" required>
                        <button class="btn btn-primary">Zapisz</button>
                    </form>
                </div>
            </div>
            <div class="text-center mt-3">© <?= date('Y') ?> Rokitki</div>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/assets/app.js"></script>
</body>
</html>

