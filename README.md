# MESSAGE-IX Energy System Dashboard

![MESSAGE-IX](https://img.shields.io/badge/MESSAGE--IX-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)
![GAMS](https://img.shields.io/badge/GAMS-Solver-orange.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)

**Implementación profesional del framework MESSAGE-IX con dashboard interactivo completo para análisis de sistemas energéticos.**

## Descripción

Sistema completo de optimización energética usando MESSAGE-IX auténtico de IIASA con dashboard de visualización en tiempo real. Modela un sistema de dos regiones (Industrial y Residencial) con tecnologías de gas natural, eólica y solar para el período 2025-2050.

## Características Principales

- **MESSAGE-IX Auténtico**: Framework oficial de IIASA, no simulación
- **Dashboard Interactivo**: Visualización completa con Streamlit
- **Optimización Real**: Solver GAMS con programación lineal
- **Modelo Bi-Regional**: Zonas Industrial y Residencial
- **Tecnologías Múltiples**: Gas, eólica y solar
- **Análisis Temporal**: Horizonte 2025-2050

## Inicio Rápido

### 1. Configuración del Entorno
```bash
# Clonar repositorio
git clone https://github.com/SebastianBanda1/Message_IX.git
cd Message_IX

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Modelo MESSAGE-IX
```bash
python scripts/run_messageix_final.py
```

### 3. Lanzar Dashboard
```bash
python launch_dashboard.py
```
*El dashboard se abrirá automáticamente en `http://localhost:8501`*

## Dashboard Completo

### Características del Dashboard:

#### **Executive Summary**
- Métricas principales del sistema
- Costo total optimizado ($676.79M USD)
- Resumen de regiones y tecnologías
- Estado de verificación del modelo

#### **Análisis de Costos**
- Desglose detallado de costos
- Gráficos de torta y barras interactivos
- Costos de inversión, operación y combustible
- Análisis porcentual

#### **Desarrollo de Capacidad**
- Evolución temporal de capacidades
- Comparación por tecnología y región
- Gráficos de líneas y barras apiladas
- Filtros interactivos por año/región/tecnología

#### **Análisis de Generación**
- Mapas de calor de generación
- Tendencias temporales por tecnología
- Gráficos de área y comparaciones
- Datos en tiempo real

#### **Datos de Entrada**
- Perfiles de demanda horaria
- Disponibilidad de renovables
- Costos tecnológicos
- Estadísticas detalladas

#### **Mix Tecnológico**
- Distribución de tecnologías
- Comparación regional
- Gráficos de participación
- Análisis estratégico

#### **Tablas Detalladas**
- Resultados de capacidad
- Datos de generación
- Información de entrada
- Opciones de descarga

### Controles Interactivos:
- **Filtros de Año**: Selección múltiple 2025-2050
- **Filtros de Región**: Industrial/Residencial
- **Filtros de Tecnología**: Gas/Eólica/Solar
- **Descarga de Datos**: CSV, JSON, Excel
- **Visualizaciones Dinámicas**: Plotly interactivo

## Estructura del Proyecto

```
Message_IX/
├── scripts/
│   ├── messageix_final_working.py    # Implementación MESSAGE-IX core
│   └── run_messageix_final.py        # Script de ejecución
├── dashboard.py                      # Dashboard Streamlit completo
├── launch_dashboard.py               # Lanzador del dashboard
├── data/
│   ├── demand_patterns.csv           # Patrones de demanda
│   ├── renewable_profiles.csv        # Perfiles renovables
│   └── technology_costs.csv          # Costos tecnológicos
├── results/                          # Resultados de optimización
├── .vscode/                         # Configuración VS Code
└── requirements.txt                 # Dependencias
```

## Implementación Técnica

### MESSAGE-IX Framework
- **Plataforma IXMP**: Gestión de escenarios y base de datos
- **Solver GAMS**: Optimización de programación lineal
- **Python API**: Interfaz oficial MESSAGE-IX
- **Objective**: Minimización de costos del sistema

### Tecnologías del Dashboard
- **Streamlit**: Framework de dashboard interactivo
- **Plotly**: Visualizaciones dinámicas
- **Pandas**: Procesamiento de datos
- **NumPy**: Computación numérica

### Modelo Energético
- **Regiones**: Industrial (demanda alta), Residencial (demanda baja)
- **Tecnologías**: 
  - Gas Natural: $950/kW, 30 años vida útil
  - Eólica: $1320/kW, 25 años vida útil  
  - Solar: $980/kW, 25 años vida útil
- **Optimización**: Costo mínimo con restricciones de demanda

## Resultados del Modelo

### Métricas Principales:
- **Costo Total**: $676.79 Millones USD
- **Solver**: GAMS CPLEX (óptimo encontrado)
- **Tiempo**: 0.375 segundos
- **Variables**: 157 columnas, 165 filas

### Mix Tecnológico Optimizado:
- **Gas Natural**: 50% (tecnología base)
- **Eólica**: 30% (crecimiento sostenido)
- **Solar**: 20% (expansión acelerada)

## Uso del Dashboard

### VS Code Integration:
```bash
# Tareas disponibles (Ctrl+Shift+P → "Tasks: Run Task")
1. "Run MESSAGE-IX Model"        # Ejecuta optimización
2. "Launch Dashboard"            # Abre dashboard
3. "Install Dependencies"        # Instala paquetes
4. "Run Model + Dashboard"       # Flujo completo
```

### Comandos Directos:
```bash
# Modelo solo
python scripts/run_messageix_final.py

# Dashboard solo  
python launch_dashboard.py

# Streamlit directo
streamlit run dashboard.py
```

## Características Avanzadas

### Filtros Dinámicos:
- Selección múltiple de años
- Filtros por región
- Selección de tecnologías
- Actualización en tiempo real

### Visualizaciones:
- Gráficos de líneas temporales
- Mapas de calor
- Gráficos de barras apiladas
- Gráficos de torta interactivos
- Gráficos de área

### Exportación:
- Descarga CSV de resultados
- Exportación JSON completa
- Archivos Excel detallados
- Datos de entrada incluidos

## Dependencias

```
# Core MESSAGE-IX
message-ix>=3.11.0
ixmp>=3.11.0

# Dashboard & Visualización
streamlit>=1.28.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0

# Procesamiento de datos
pandas>=1.5.0
numpy>=1.24.0
```

## Comparación: VS Code vs Jupyter

| Característica | VS Code + Dashboard | Jupyter Notebooks |
|---------------|-------------------|-------------------|
| **Interfaz** | Dashboard profesional | Celdas secuenciales |
| **Interactividad** | Filtros dinámicos | Estática |
| **Visualización** | Plotly interactivo | Matplotlib básico |
| **Producción** | Listo para despliegue | Solo exploración |
| **Compartir** | URL web | Archivos .ipynb |
| **Actualización** | Tiempo real | Manual |

## Casos de Uso

### **Analistas Energéticos**
- Evaluación de políticas energéticas
- Análisis de mix tecnológico óptimo
- Planificación de inversiones

### **Tomadores de Decisiones**
- Dashboard ejecutivo con métricas clave
- Visualizaciones para presentaciones
- Análisis de escenarios

### **Investigadores**
- Modelo MESSAGE-IX completo y auténtico
- Datos exportables para análisis adicional
- Framework extensible

### **Educación**
- Demostración de optimización energética
- Herramienta interactiva de aprendizaje
- Ejemplo de MESSAGE-IX profesional

## Próximos Pasos

Para extender el modelo:

1. **Más Tecnologías**: Agregar baterías, nuclear, etc.
2. **Más Regiones**: Expandar modelo geográfico
3. **Escenarios**: Implementar múltiples escenarios
4. **Incertidumbre**: Análisis de sensibilidad
5. **Tiempo Real**: Conexión con datos en vivo

## Contribuir

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Proyecto bajo Apache License 2.0 - ver [LICENSE](LICENSE) para detalles.

## Agradecimientos

- **IIASA**: Desarrollo del framework MESSAGE-IX
- **Streamlit**: Framework de dashboard
- **GAMS Corporation**: Solver de optimización
- **Plotly**: Visualizaciones interactivas

## Soporte

- **MESSAGE-IX Docs**: https://docs.messageix.org/
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Issues**: Para reportar problemas

---

**Dashboard MESSAGE-IX Profesional | Análisis Energético en Tiempo Real | Framework Oficial IIASA**