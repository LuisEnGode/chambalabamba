#!/bin/bash

# Lista de apps a crear
apps=("filosofia" "saberes" "escuela" "eventos" "hospedaje" "voluntariado" "donaciones" "tienda" "noticias" "contacto")

for app in "${apps[@]}"
do
  echo "Creando app: $app"
  python manage.py startapp $app

  # Crear carpetas estándar
  mkdir -p $app/templates/$app
  mkdir -p $app/static/$app/css
  mkdir -p $app/static/$app/js
  mkdir -p $app/static/$app/images
  mkdir -p $app/templatetags

  # Crear __init__.py en templatetags
  touch $app/templatetags/__init__.py
  echo "# Custom template tags para $app" > $app/templatetags/${app}_tags.py

  # Crear urls.py básico
  cat > $app/urls.py <<EOF
from django.urls import path
from . import views

app_name = '$app'

urlpatterns = [
    path('', views.index, name='index'),
]
EOF

  # Agregar vista inicial en views.py
  echo -e "\n\ndef index(request):\n    return render(request, '$app/index.html')" >> $app/views.py

  # Crear template base
  echo "<h1>$app</h1>" > $app/templates/$app/index.html

done

echo "✅ Todas las apps fueron creadas."

