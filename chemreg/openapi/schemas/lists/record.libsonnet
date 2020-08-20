local list = import 'list.libsonnet';
local substance = import 'substance/substance.libsonnet';
 
 {
  app: 'Lists',
  type: 'record',
  description: 'Everything about Records.',
  attributes: {
    rid: {
      type: 'string',
      maxLength: 50,
      unique: true,
    },
    external_id: {
      type: 'string',
      maxLength: 500,
      required: true,
    },
    score: {
      type: 'float',
    },
    message: {
      type: 'string',
      maxLength: 500,
    },
    is_validated: {
      type: 'boolean',
    },
  },
  relationships: [
    {
      object: list + 
        { 
          relationships: [] 
        },
      many: false,
      default: 1,
    },
    {
      object: substance + 
        { 
          relationships: [] 
        },
      many: false,
      default: 1,
    },
  ]
} 