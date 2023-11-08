# **Startup-ARD-01**
**MODULO RELÉ**
Código del funcionamiento del modulo relé a través del monitor serial, con Arduino:

```mermaid
graph LR
A[Encender Bomba] -- Enviar al monitor serial --> B((1))
C[Apagar Bomba] -- Enviar al monitor serial --> D((0))