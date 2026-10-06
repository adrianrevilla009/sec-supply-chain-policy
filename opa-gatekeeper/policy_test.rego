package orders.k8s_test

import data.orders.k8s
import rego.v1

good := {"spec": {"containers": [{"name": "a", "image": "orders:1.0", "securityContext": {"runAsNonRoot": true}}]}}
bad := {"spec": {"containers": [{"name": "a", "image": "orders:latest"}]}}

test_good_allowed if count(k8s.deny) == 0 with input as good
test_bad_denied if count(k8s.deny) == 2 with input as bad
