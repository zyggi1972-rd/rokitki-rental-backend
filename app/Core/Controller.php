<?php
namespace App\Core;

class Controller
{
    protected array $config;

    public function __construct(array $config)
    {
        $this->config = $config;
        date_default_timezone_set($config['app']['timezone'] ?? 'UTC');
    }

    protected function render(string $view, array $params = [], string $layout = 'main'): void
    {
        extract($params, EXTR_SKIP);
        $baseUrl = $this->config['app']['base_url'] ?? '';
        $viewFile = BASE_PATH . '/app/Views/' . $view . '.php';
        $layoutFile = BASE_PATH . '/app/Views/layouts/' . $layout . '.php';
        ob_start();
        require $viewFile;
        $content = ob_get_clean();
        require $layoutFile;
    }

    protected function redirect(string $url): void
    {
        header('Location: ' . $url);
        exit;
    }

    protected function isLoggedIn(): bool
    {
        return isset($_SESSION['user_id']);
    }

    protected function currentUserId(): ?int
    {
        return $_SESSION['user_id'] ?? null;
    }

    protected function requireAuth(): void
    {
        if (!$this->isLoggedIn()) {
            $_SESSION['redirect_after_login'] = $_SERVER['REQUEST_URI'] ?? '/';
            $this->redirect('/login');
        }
    }

    protected function requireAdmin(): void
    {
        $this->requireAuth();
        if (($_SESSION['role'] ?? 'user') !== 'admin') {
            http_response_code(403);
            echo 'Forbidden';
            exit;
        }
    }
}

