version 1.0
## It is not complete yet
task createDrsComplianceReport{
    
    input {
        String server
        String json_path
    }

    command {
        drs-compliance --server_base_url ${server} --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --auth_type "none" --report_path ${json_path}
    }

    output {
        File drs_compliance_report = "${json_path}"
    }

    runtime {
        docker: "ga4gh/drs-compliance-suite:test"
    }

}

workflow drsComplianceReportWorkflow {

    input {
        String server
        String json_path
    }

    call createDrsComplianceReport { input: server=server, json_path=json_path }

}