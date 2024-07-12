import http from 'k6/http';
import { sleep, check } from "k6";

export default function() {
    let server_list = ['http://127.0.0.1:8000/',
    let endpoint_list = ['/user']

    server_list.forEach(server => {
        endpoint_list.forEach(endpoint => {
            let res = http.get(server + endpoint)
            check(res, { 'status was 200': (r) => r.status == 200 });
        });
    }

    sleep(0.3)
}
