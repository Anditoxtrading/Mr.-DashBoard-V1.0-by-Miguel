# Mr. DashBoard - Bybit Futures Dashboard

![Mr. DashBoard](https://your-image-url.com/banner.png)  

## Descripción 📊

**Mr. DashBoard** es una aplicación desarrollada en **Python** con **Dash** que permite visualizar y analizar datos de operaciones en **Bybit Futures**. Utiliza la API de Bybit para obtener información sobre:

- PnL (**Profit and Loss**)
- Operaciones ganadas y perdidas
- Distribución de monedas operadas
- Gráficos interactivos para mejorar el análisis de trading

---

## 🚀 Requisitos

Para ejecutar esta aplicación, instala las siguientes dependencias con **pip**:

```bash
pip install dash dash-bootstrap-components plotly pybit
```

---

## ⚙️ Configuración

1. **Clona este repositorio** o descarga los archivos del proyecto:
   ```bash
   git clone https://github.com/tu-usuario/Mr-DashBoard.git
   cd Mr-DashBoard
   ```

2. **Configura las credenciales de API** de Bybit:
   - Crea un archivo `config.py` en la raíz del proyecto.
   - Agrega las siguientes líneas con tus credenciales:
     ```python
     api_key = "TU_API_KEY"
     api_secret = "TU_API_SECRET"
     ```

🔴 **IMPORTANTE:** Nunca compartas tus credenciales en repositorios públicos.

---

## ▶️ Ejecución

Para iniciar la aplicación, ejecuta:

```bash
python nombre_del_script.py
```

Luego, abre tu navegador y accede a:  
📌 **[http://127.0.0.1:8050/](http://127.0.0.1:8050/)** para ver el dashboard en acción.

---

## 📌 Funcionalidades

✅ Consulta de **PnL** en un rango de fechas determinado.  
✅ Visualización de **operaciones ganadas y perdidas**.  
✅ **Gráficos interactivos** de distribución de ganancias y pérdidas.  
✅ Análisis de **PnL por horas y días de la semana**.  
✅ Identificación de **las monedas más rentables**.  

---


