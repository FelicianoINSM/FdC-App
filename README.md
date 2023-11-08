# **Startup-ARD-01**
**MÓDULO RELÉ**
Código del funcionamiento del módulo relé a través del monitor serial, con Arduino:

```mermaid
graph LR
A[Encender Bomba] -- Enviar al monitor serial --> B((1))
C[Apagar Bomba] -- Enviar al monitor serial --> D((0))
```
#
**MÓDULO SENSOR DE HUMEDAD DEL SUELO**
Código del funcionamiento del módulo de humedad del suelo a través del monitor serial, con Arduino:
```mermaid
graph LR
A[Suelo 100% seco] -- El monitor serial mostrará--> B((1023))
C[Suelo 100% hÚmedo] -- El monitor serial mostrará --> D((0))
```
#