package orders.k8s

import rego.v1

deny contains msg if {
	some c in input.spec.containers
	endswith(c.image, ":latest")
	msg := sprintf("container %s uses the latest tag", [c.name])
}

deny contains msg if {
	some c in input.spec.containers
	not c.securityContext.runAsNonRoot
	msg := sprintf("container %s must set runAsNonRoot", [c.name])
}
