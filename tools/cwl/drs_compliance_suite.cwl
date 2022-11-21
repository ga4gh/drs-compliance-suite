#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand:
hints:
  DockerRequirement:
    dockerPull: ga4gh/drs-compliance-suite:test
inputs:
  server_base_url:
    type: string
    inputBinding:
      position: 1
      prefix: --server_base_url
  platform_name:
    type: string
    inputBinding:
      position: 2
      prefix: --platform_name
  platform_description:
    type: string
    inputBinding:
      position: 3
      prefix: --platform_description
  auth_type:
    type: string
    inputBinding:
      position: 4
      prefix: --auth_type
  report_path:
    type: string
    inputBinding:
      position: 5
      prefix: --report_path
outputs: 
  drs-compliance-report:   
    type: File
    outputBinding:
      glob: $(inputs.report_path)