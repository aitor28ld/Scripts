# ansible-configuration directory
Script hecho en Python para instalar y tener lista la configuración inicial para empezar a usar Ansible.

Funciones que realiza el script:
- Comprueba si el usuario que lo ejecuta, tiene configurada las claves SSH, sino las crea.
- Actualiza la paquetería del sistema para obtener la última lista de repositorios.
- Instala Ansible si no está ya instalado.
- Crea el directorio dónde se guardarán los logs de Ansible
- Se crea un backup de los ficheros de configuración que Ansible configura por defecto.
- El script pregunta por un host y su IP para configurarlo en Ansible y así empezar a usarlo

**NOTA**: solo se configura un host, para añadir más hosts edita el fichero /etc/ansible/hosts
