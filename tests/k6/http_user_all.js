import http from 'k6/http';
import { check, sleep } from 'k6';
import { URL } from 'https://jslib.k6.io/url/1.0.0/index.js';

export default function() {
    const url = new URL("http://127.0.0.1:8000/users");
    url.searchParams.append('skip', '0');
    url.searchParams.append('limit', '100');

    const res = http.get(url.toString())
    // console.log(res.json());

    check(res, { 'status was 200': (r) => r.status == 200 });
    sleep(0.3)
}
