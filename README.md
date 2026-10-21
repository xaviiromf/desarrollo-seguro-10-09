# Supermercado: listas de compras (Django)

CRUD de listas de compras con productos, cantidades y precios en CLP. Cada usuario ve solo sus propias listas.

- Producción: https://actividaddjango1.pythonanywhere.com
- Guía de despliegue: `PYTHONANYWHERE_DEPLOY.md`
- Entrega de la Evaluación U2 (Desarrollo Seguro): `evaluacion_u2/`

## Ejecutar en local

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # genera una SECRET_KEY propia (ver el comentario del archivo)
python manage.py migrate
python manage.py test shopping
python manage.py runserver
```

## Checklist de 5 minutos antes de cada push

1. **¿Hay secretos en el diff?** Revisa `git diff --staged` en busca de `SECRET_KEY`, contraseñas o tokens. El `.env` nunca se sube.
2. **¿La configuración de despliegue está bien?** Ejecuta `python manage.py check --deploy` con las variables de producción.
3. **¿Las pruebas están en verde?** Ejecuta `python manage.py test shopping`.
4. **¿El `.env` sigue fuera de git?** `git ls-files | grep -x .env` no debe devolver nada.

Si encuentras un secreto ya subido, no basta con borrarlo: hay que rotarlo.
