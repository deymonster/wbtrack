// PrometheusService.js
import axios from 'axios';

const PROMETHEUS_URL = "http://192.168.13.71:9090/api/v1/query_range";

const getCpuTemperatureOverTime = async ({start, end, step}) => {

    const params = {
        query: "cpu_temperature",
        start,
        end,
        step
    };

    try {
        const response = await axios.get(PROMETHEUS_URL, { params});
        if (response.data.status === 'success') {
            return response.data.data.result;
        } else {
            throw new Error('Failed to fetch data from Prometheus');
        }
    } catch (error) {
        console.error('Error fetching data from Prometheus:', error);
        throw error;
    }
};

export default  getCpuTemperatureOverTime;
