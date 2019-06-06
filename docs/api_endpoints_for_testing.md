
| Tables   |      Are      |  Cool |
|----------|:-------------:|------:|
| col 1 is |  left-aligned | $1600 |
| col 2 is |    centered   |   $12 |
| col 3 is | right-aligned |    $1 |

| foo | bar |
| --- | --- |
| baz | bim |


|      NAME      | Description                |     Details                          |  API/UI     |   Category  |
|--------------- | -------------------        | -------------------------------------|-------------| ----------- |
| override_api	 | Test override API’s        |	organization_list                    |  API        |     Ext     |
|                |                            |    get_msg_content                   |             |             |
|                |                            |    add_msg_niceties                  |             |             |
|                |                            |    send_state_change_notifications   |             |             |
|                |                            |    check_record_state                |             |             |
|                |                            |    edc_package_update                |             |             |
|                |                            |    edc_package_update_bcgw           |             |             |
|                |                            |    package_update                    |             |             |
|                |                            |    package_autocomplete	             |             |             |
| crud_dataset	 | Create/update/search/purge | 	                                 | API         |  CORE       |
| frontend_api	 | CKAN api calls that are used by the front end, verify that the data schema has not changed |	"/api/3/action/package_search?" | API         |  CORE|  
|                |                            | "/api/3/action/package_show"         |             |             |
|                |                            | "/api/3/action/package_update"       |             |             |
|                |                            | "/api/3/action/organization_show"    |             |             |
|                |                            | "/api/3/action/organization_list_related?all_fields=True" |             |             |
|                |                            | "/api/3/action/dashboard_activity_list" |             |             |
|                |                            | "/api/3/action/user_show?id="+req.params.userId+"&include_datasets=True" |             |             |
|                |                            | "/api/3/action/tag_list"             |             |             |
|                |                            | "/api/3/action/vocabulary_list"      |             |             |
|                |                            | "/api/3/action/license_list"         |             |             |
|                |                            | "/api/3/action/group_list?all_fields=true" |             |             |
|                |                            | "/api/3/action/group_show?id="+req.params.id+"&include_datasets=true" |             |             |
|                |                            | "/api/3/action/config_option_show?key=ckan.site_about"	API	CORE |             |             |
| editor_write_permissions |	test editor access	 | |	API	| Access/Security |
| public_write_permissions |	test public access	 	| | API |	Access/Security |
| view_record_permissions |	check idir or public can view record	| | 	API | Access/Security |
