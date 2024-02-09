from google.cloud import dataplex_v1

def get_job_results():
    # Create a Dataplex client object
    print("Authenticating Dataplex Client...")
    client = dataplex_v1.DataScanServiceClient()

    # Set a GetDataScanRequest() using the args.datascan_name argument.
    datascan_name = "projects/446454295341/locations/us-central1/dataScans/a9e80829b-9152-48f3-9c4c-c3741d7f0deb/jobs/b63c1f54-b268-42b2-b774-687666d000ec"
    request_scan = dataplex_v1.GetDataScanRequest(name="projects/446454295341/locations/us-central1/dataScans/a9e80829b-9152-48f3-9c4c-c3741d7f0deb/jobs/b63c1f54-b268-42b2-b774-687666d000ec")
    response_scan = client.get_data_scan(request=request_scan)
    print("Got to here i received a response")

    # print("RESPONSE_SCAN-->")
    # print(response_scan)

    dq_scan_name = response_scan.name

    parse_data_scan_path = client.parse_data_scan_path(datascan_name)
    dq_project = parse_data_scan_path.get('project')
    dq_scan_id = parse_data_scan_path.get('dataScan')

    table_reference = response_scan.data.resource
    if table_reference == '':
        table_reference = response_scan.data.entity
    dq_table = table_reference.split("/")[-1]

    request = dataplex_v1.ListDataScanJobsRequest(
        parent=datascan_name,
        page_size=10)
        # optional: filter, page_size

    page_result = client.list_data_scan_jobs(request=request)
    counter = 0
    job_names = []
    for response in page_result:
        counter += 1
        job_names.append(response.name)

    print('Jobs scanned: ' + str(counter))

    # Read Jobs data
    for job_name in job_names:
        job_request = dataplex_v1.GetDataScanJobRequest(
            name=job_name,
            view="FULL",
        )
        job_result = client.get_data_scan_job(request=job_request)
        # Skips jobs if not in succeeded state
        if job_result.state != 4:
            continue

        dq_job_id = job_result.uid

        passing_rules = 0
        failing_rules = 0
        for rule in job_result.data_quality_result.rules:
            if rule.passed is True:
                passing_rules += 1
            elif rule.passed is False:
                failing_rules += 1
        
        print(' -->Passing rules = ' + str(passing_rules))
        print(' -->Failing rules = ' + str(failing_rules))
        
        print("dq_scan_name --> " + dq_scan_name)
        print("dq_scan_id --> " + dq_scan_id)
        print("dq_table --> " + dq_table)
        print("dq_project --> " + dq_project)
        print("dq_job_id --> " + dq_job_id)
        print("job_result.data_quality_result.row_count --> " + str(job_result.data_quality_result.row_count))
        print("job_result.data_quality_result.passed --> " + str(job_result.data_quality_result.passed))
        print("len(job_result.data_quality_result.rules) --> " + str(len(job_result.data_quality_result.rules)))
        print("passing_rules --> " + str(passing_rules))
        print("job_result.start_time --> " + str(job_result.start_time))
        print("job_result.end_time --> " + str(job_result.end_time))
        print("MessageToJson(job_result.data_quality_result.scanned_data._pb) --> " + MessageToJson(job_result.data_quality_result.scanned_data._pb))
        print("MessageToJson(job_result.data_quality_result._pb) --> " + MessageToJson(job_result.data_quality_result._pb))

        for rule_result in job_result.data_quality_result.rules:
            MessageToJson(rule_result.rule._pb)
            rule_result.rule.dimension
            rule_result.passed
            rule_result.pass_ratio
            rule_result.failing_rows_query
        
        print("MessageToJson(rule_result.rule._pb) --> " + MessageToJson(rule_result.rule._pb))
        print("rule_result.rule.dimension --> " + rule_result.rule.dimension)
        print("rule_result.passed --> " + str(rule_result.passed))
        print("rule_result.pass_ratio --> " + str(rule_result.pass_ratio))
        print("rule_result.failing_rows_query --> " + rule_result.failing_rows_query)
            

get_job_results()