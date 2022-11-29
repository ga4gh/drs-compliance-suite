version 1.0
## It is not complete yet
task createDrsComplianceReport{
    
    input {
        String server_base_url
        String platform_name
        String platform_description
        String report_path
    }

    command {
        drs-compliance --server_base_url ${server_base_url} --platform_name "${platform_name}" --platform_description "${platform_description}" --auth_type "none" --report_path "${report_path}"
    }

    output {
        File drs_compliance_report = "${report_path}"
    }

    runtime {
        docker: "ga4gh/drs-compliance-suite:test"
    }

}

workflow drsComplianceReportWorkflow {

    input {
        String server_base_url
        String platform_name
        String platform_description
        String report_path
    }

    call createDrsComplianceReport { 
        input: server_base_url=server_base_url, platform_name=platform_name, platform_description=platform_description, report_path=report_path
    }
}