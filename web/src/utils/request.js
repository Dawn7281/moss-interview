import axios from 'axios';

class HttpRequest {
    constructor() {
        this.baseUrl = 'http://localhost:5000';
        // this.baseUrl = 'https://www.moss-interviewer.website';
    }

    getInsideConfig() {
        const config = {
            baseURL: this.baseUrl,
            timeout: 500000,
            withCredentials: true,
            headers: {
                // 设置后端需要的传参类型
                // 'Content-Type': 'application/json',
                // 'token': x-auth-token',//一开始就要token
                // 'X-Requested-With': 'XMLHttpRequest',
            },
            validateStatus: (status) => {
                return (status >= 200 && status < 300) || status === 400;
            }
        };
        return config;
    }

    interceptors(instance) {
        instance.interceptors.request.use(
            (config) => {
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );

        instance.interceptors.response.use(
            (res) => {
                // const { data } = res;
                console.log('返回数据处理', res);
                return res;
            },
            (error) => {
                console.log('error==>', error);
                return Promise.reject(error);
            }
        );
    }

    request(options) {
        const instance = axios.create();
        options = Object.assign(this.getInsideConfig(), options);
        this.interceptors(instance);
        return instance(options);
    }
}

const http = new HttpRequest();
export default http;