schema_get_by_status = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "integer"
      },
      "category": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name"
        ]
      },
      "name": {
        "type": "string"
      },
      "photoUrls": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "tags": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            }
          }
        }
      },
      "status": {
        "type": "string"
      }
    },
    "required": [
      "name",
      "photoUrls"
    ]
  }
}


schema_get_by_id = {
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    },
    "name": {
      "type": "string"
    },
    "category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        }
      }
    },
    "photoUrls": {
      "type": "array",
      "items":
        {
          "type": "string"
        }
    },
    "tags": {
      "type": "array",
      "items":
        {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            }
          }
        }
    },
    "status": {
      "type": "string"
    }
  },
  "required": [
    "photoUrls",
    "name"
  ]
}
