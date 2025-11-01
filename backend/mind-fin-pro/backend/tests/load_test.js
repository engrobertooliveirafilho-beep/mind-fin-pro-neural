import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 150,
  duration: "60s",
  thresholds: {
    http_req_duration: ["p(95)<250"],
  },
};

export default function () {
  const res = http.get("http://localhost:8000/health");
  check(res, { "status é 200": (r) => r.status === 200 });
  sleep(1);
}
