# Climate Change Impact Dashboard

An interactive dashboard built with Dash and Plotly that visualizes climate change data, including global temperature trends, CO2 emissions by country, and extreme weather events.

## Data Analysis Summary

The dashboard reveals several critical insights about climate change and its global impact:

### Temperature Trends Analysis
Global temperature data shows a clear warming trend since the industrial revolution, with an accelerated increase post-1950. The data indicates an approximate 1.0°C rise in global average temperatures since pre-industrial times, with the most rapid warming occurring in recent decades. This trend aligns with the rise in industrial activity and greenhouse gas emissions, suggesting a strong correlation between human activities and global warming.

### CO2 Emissions Patterns
The emissions data highlights significant disparities in CO2 output among major economies. China and the United States emerge as the largest emitters, with China showing a dramatic increase since 2000 coinciding with its rapid industrialization. While developed nations like the United States and Japan show relatively stable or slightly declining emissions in recent years, developing economies like India demonstrate steadily increasing trends. This pattern reflects the complex challenge of balancing economic development with environmental sustainability.

### Weather Events Correlation
The analysis of extreme weather events reveals an increasing frequency and intensity of climate-related incidents. There's a notable uptick in severe weather events since the 1980s, particularly in:
- Heat waves and extreme temperature events
- High-intensity precipitation and flooding
- Severe storms and cyclonic activity
This trend correlates with rising global temperatures, suggesting a direct link between climate change and extreme weather phenomena.

### Key Takeaways
1. The data provides strong evidence of human-induced climate change, demonstrated by the parallel rise in temperatures and CO2 emissions.
2. There's an urgent need for global cooperation in emissions reduction, considering the varying stages of economic development across nations.
3. The increase in extreme weather events underscores the immediate impacts of climate change on human societies and ecosystems.
4. Recent trends in some developed nations show that economic growth can be maintained while reducing emissions, offering a potential model for sustainable development.

## Features

- **Global Temperature Trends**
  - Interactive date range selection (1880-2024)
  - Historical temperature data visualization
  - Temperature anomaly tracking

- **CO2 Emissions by Country**
  - Multi-country selection
  - Customizable date range
  - Per-country emissions tracking
  - Interactive legends and tooltips

- **Extreme Weather Events**
  - Event type filtering
  - Temporal trend analysis
  - Frequency visualization
  - Custom date range selection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MikeWarsowski/climate-change-dashboard.git
cd climate-change-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python minimal_app.py
```

4. Open your web browser and navigate to:
```
http://localhost:8501
```

## Data Sources

The dashboard uses the following datasets:
- Temperature data: Historical global temperature records
- CO2 emissions data: Country-wise CO2 emissions over time
- Weather events data: Historical extreme weather event records

## Technologies Used

- Python 3.x
- Dash
- Plotly
- Pandas
- Bootstrap (via dash-bootstrap-components)

## Contributing

Feel free to fork the repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 