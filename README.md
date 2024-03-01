# CashToday-Quetzalfir

## Descripción

`CashToday-Quetzalfir` es una solución diseñada para permitir el envío de remesas online desde Estados Unidos hacia diferentes países de LATAM a través de una aplicación web. Este proyecto fue desarrollado como parte de una prueba técnica para la posición de Arquitecto de Soluciones, con el objetivo de integrar servicios de backend a una nueva aplicación web para CashToday. La solución incluye una API serverless que proporciona los endpoints necesarios para realizar la búsqueda de clientes, además de manejar la adición, modificación y eliminación de estos.

## Diagramas

### Diagrama de Flujo

![Diagrama de Flujo](/documents/image/Flow.png)

### Solución AWS

![Solución AWS](/documents/image/Solution.png)

### Modelo de Datos

![Modelo de Datos](/documents/image/Model.png)

## Requerimientos Adicionales

Además de las dependencias ya incluidas en `requirements.txt`, es importante considerar la inclusión de librerías adicionales que faciliten la integración con AWS, como `boto3` para la interacción programática con los servicios de AWS, y `aws-cdk` para la infraestructura como código, si aún no están incluidas.

## Uso de Comandos

### CDK Bootstrap

```bash
cdk bootstrap --context env=dev --profile tw-dev-devops
```
Este comando prepara el entorno de desarrollo (dev) para el despliegue de la infraestructura con AWS CDK, utilizando el perfil de AWS tw-dev-devops.

### CDK Deploy
```bash
cdk deploy CashTodayStack-Dev --context env=dev --profile cashToday-dev-devops
```
Despliega la pila CashTodayStack-Dev en el entorno de desarrollo (dev), usando el perfil cashToday-dev-devops. Esto crea o actualiza recursos en AWS según la definición de la pila.

## Uso de Colecciones y Entornos Postman
![Modelo de Datos](/documents/image/postman.png)
Para probar la API mediante Postman, sigue estos pasos:

Descarga los archivos de colección y ambiente de la carpeta postman.
Abre Postman y selecciona "Import" para importar tanto la colección como el ambiente.
Selecciona el ambiente importado desde la esquina superior derecha para activarlo.
Puedes comenzar a hacer solicitudes a la API seleccionando los endpoints definidos en la colección y ajustando los parámetros según sea necesario.
Tokens de Acceso a las APIs

### Para utilizar los endpoints de la API, necesitarás tokens de acceso para cada uno de los ambientes (dev, uat, prod). Los tokens son:

Desarrollo (dev): 123456

Pruebas de Aceptación del Usuario (uat): abcdef

Producción (prod): a1b2c3

