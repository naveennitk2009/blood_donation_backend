def get_coupon_mapping():
	body = {
		"coupon": {
			"properties": {
				"discount": {
					"type": "string"
				},
				"merchant": {
					"type": "string"
				},
				"short_description": {
					"type": "string"
				},
				"description": {
					"type": "string"
				},
				"code": {
					"type": "string"
				},
				"validity": {
					"type": "date"
				},
				"tags": {
					"type": "string"
				}
			}
		}
	}
	return body