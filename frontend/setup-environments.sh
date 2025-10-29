#!/bin/bash

echo "🔧 Setting up Angular environments..."

# Create environments directory
docker exec -it news_frontend sh -c "mkdir -p /app/src/environments"

# Create environment.ts (development)
docker exec -it news_frontend sh -c "cat > /app/src/environments/environment.ts << 'ENVEOF'
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  newsApiKey: '',
  logLevel: 'debug',
  enableCache: true,
  cacheTTL: 180,
  version: '1.0.0',
  appName: 'News Dashboard'
};
ENVEOF"

# Create environment.prod.ts (production)
docker exec -it news_frontend sh -c "cat > /app/src/environments/environment.prod.ts << 'ENVEOF'
export const environment = {
  production: true,
  apiUrl: '/api',
  newsApiKey: '',
  logLevel: 'error',
  enableCache: true,
  cacheTTL: 300,
  version: '1.0.0',
  appName: 'News Dashboard'
};
ENVEOF"

echo "✅ Environment files created!"
echo ""
echo "📁 Files created:"
docker exec -it news_frontend sh -c "ls -la /app/src/environments/"

echo ""
echo "�� Next steps:"
echo "1. Update angular.json with fileReplacements"
echo "2. Import environment in your services: import { environment } from '../environments/environment';"
echo "3. Build with: ng build --configuration=production"

