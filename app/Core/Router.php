<?php
namespace App\Core;

class Router
{
    private array $routes = [];
    private array $config;

    public function __construct(array $config)
    {
        $this->config = $config;
    }

    public function get(string $path, $handler): void
    {
        $this->add('GET', $path, $handler);
    }

    public function post(string $path, $handler): void
    {
        $this->add('POST', $path, $handler);
    }

    public function any(string $path, $handler): void
    {
        $this->add('GET', $path, $handler);
        $this->add('POST', $path, $handler);
    }

    private function add(string $method, string $path, $handler): void
    {
        $this->routes[$method][] = ['path' => $path, 'handler' => $handler];
    }

    public function dispatch(string $method, string $uri)
    {
        $path = parse_url($uri, PHP_URL_PATH) ?? '/';
        $routes = $this->routes[$method] ?? [];
        foreach ($routes as $route) {
            $pattern = '@^' . preg_replace('@\{([\w]+)\}@', '(?P<$1>[^/]+)', rtrim($route['path'], '/')) . '$@D';
            if (preg_match($pattern, rtrim($path, '/'), $matches)) {
                $params = array_filter($matches, 'is_string', ARRAY_FILTER_USE_KEY);
                return $this->invoke($route['handler'], $params);
            }
        }
        http_response_code(404);
        echo '404 Not Found';
        return null;
    }

    private function invoke($handler, array $params)
    {
        if (is_callable($handler)) {
            return call_user_func_array($handler, $params);
        }
        if (is_string($handler) && strpos($handler, '@') !== false) {
            [$controller, $method] = explode('@', $handler, 2);
            $class = 'App\\Controllers\\' . $controller;
            if (class_exists($class)) {
                $instance = new $class($this->config);
                if (method_exists($instance, $method)) {
                    return call_user_func_array([$instance, $method], $params);
                }
            }
        }
        throw new \RuntimeException('Invalid route handler');
    }
}

