# Crear Dockerfile correcto
FROM node:20-alpine

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci --quiet

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 4300

# Comando de inicio
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4300", "--poll", "1000"]
