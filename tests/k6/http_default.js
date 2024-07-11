import http from 'k6/http';
import { sleep, check, fail } from "k6";

export default function() {
    let res = http.get("http://127.0.0.1:8000/")

    check(res, { 'status was 200': (r) => r.status == 200 });
//    if (!check(res, {
//        'is statuscode 200 - endpoint news': (r) => r.status === 200
//    })) {
//        fail('Falha na execução do cenário de teste news');
//    }

    sleep(0.3)
}
