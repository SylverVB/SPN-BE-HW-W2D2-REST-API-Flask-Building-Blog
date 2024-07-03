# REST API Design Patterns

### REST Resource Naming Conventions
1. Use nouns for resource names
    - `/galleries`
    - `/posts`
    - `/users`
2. Use plural nouns for collection names
    - `/galleries`
    - `/orders`
    - `/customers`
3. Not using singular nouns for resource names
    - `/galleries/{id}`
    - `/posts/{id}`
    - `/users/{id}`
4. Use hyphens to separate words
    - `/galleries-categories`
    - `/post-reviews`
5. Use lowercase letters
    - `/galleries`
    - `/posts`
    - `/users`
6. Use query params for filtering, sorting, and pagination
    - `/galleries?category=space`
    - `/posts?sort=subject`
    - `/posts?limit=10&offset=20`