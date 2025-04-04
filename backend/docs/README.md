# Documentación de la API

Este directorio contiene la documentación de la API del sistema de gestión de tareas.

## OpenAPI/Swagger

La documentación principal de la API está en formato OpenAPI 3.0.0 (anteriormente conocido como Swagger) en el archivo `openapi.yaml`. Esta documentación puede ser visualizada y probada usando herramientas como:

- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Redoc](https://redocly.github.io/redoc/)
- [Postman](https://www.postman.com/)

### Visualización de la Documentación

Para visualizar la documentación de forma interactiva, puedes:

1. Usar el editor online de Swagger:
   - Visita [Swagger Editor](https://editor.swagger.io/)
   - Copia y pega el contenido de `openapi.yaml`

2. Usar Redoc (recomendado para documentación estática):
   ```bash
   npx redoc-cli serve openapi.yaml
   ```

3. Integrar Swagger UI en tu aplicación:
   ```html
   <!DOCTYPE html>
   <html>
     <head>
       <title>Task Manager API</title>
       <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
     </head>
     <body>
       <div id="swagger-ui"></div>
       <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
       <script>
         window.onload = function() {
           SwaggerUIBundle({
             url: "/docs/openapi.yaml",
             dom_id: '#swagger-ui'
           })
         }
       </script>
     </body>
   </html>
   ```

## Estructura de la Documentación

La documentación está organizada en las siguientes secciones:

1. **Información General**
   - Título y descripción de la API
   - Versión
   - Información de contacto

2. **Servidores**
   - URLs de producción y desarrollo
   - Configuración de entornos

3. **Autenticación**
   - Esquema de autenticación JWT
   - Endpoint de login
   - Manejo de tokens

4. **Modelos de Datos**
   - Task (Tarea)
   - LoginRequest/Response
   - Error

5. **Endpoints**
   - Autenticación
     - POST /login
   - Tareas
     - GET /tasks
     - POST /tasks
     - GET /tasks/{taskId}
     - PUT /tasks/{taskId}
     - DELETE /tasks/{taskId}

## Ejemplos de Uso

### Autenticación

```bash
# Obtener token
curl -X POST http://localhost:3000/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Usar token en requests
curl -X GET http://localhost:3000/v1/tasks \
  -H "Authorization: Bearer <token>"
```

### Crear Tarea

```bash
curl -X POST http://localhost:3000/v1/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar autenticación",
    "description": "Agregar sistema de autenticación JWT",
    "status": "pending"
  }'
```

### Actualizar Tarea

```bash
curl -X PUT http://localhost:3000/v1/tasks/<task_id> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## Códigos de Estado HTTP

La API utiliza los siguientes códigos de estado HTTP:

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Recurso eliminado exitosamente
- `400 Bad Request`: Solicitud mal formada
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: No autorizado
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Error de validación
- `500 Internal Server Error`: Error del servidor

## Manejo de Errores

Todos los errores siguen el siguiente formato:

```json
{
  "error": {
    "message": "Mensaje descriptivo del error",
    "type": "TipoDeError",
    "details": {
      "campo": "Descripción del error"
    }
  }
}
```

## Mejores Prácticas

1. **Autenticación**
   - Siempre incluye el token JWT en el header `Authorization`
   - Los tokens expiran después de 30 minutos
   - Renueva el token antes de que expire

2. **Manejo de Errores**
   - Revisa el campo `error.type` para identificar el tipo de error
   - Usa el campo `error.details` para información específica de validación
   - Implementa reintentos para errores 5xx

3. **Validación**
   - Valida los datos antes de enviarlos
   - Revisa los campos requeridos
   - Usa los valores enumerados para el campo `status`

4. **Rate Limiting**
   - Implementa un límite de 100 requests por minuto por IP
   - Usa el header `X-RateLimit-Remaining` para monitorear el límite 