from mstrio.utils.helper import response_handler


def report_definition(connection, report_id, verbose=False):
    """
    Get the definition of a specific report, including attributes and metrics. This in-memory report definition provides information about all available objects without actually running any data query/report. The results can be used by other requests to help filter large datasets and retrieve values dynamically, helping with performance and scalability.

    Args:
        connection: MicroStrategy REST API connection object
        report_id (str): Unique ID of the report you wish to extract information from.
        verbose (bool): Verbosity of request response; defaults to False.

    Returns:
        Complete HTTP response object.
    """

    response = connection.session.get(url=connection.base_url + '/api/v2/reports/' + report_id)
    if verbose:
        print(response.url)
    if not response.ok:
        response_handler(response, "Error getting report definition. Check report ID.")
    return response


def report_instance(connection, report_id, body={}, offset=0, limit=5000, verbose=False):
    """
    Get the results of a newly created report instance. This in-memory report instance can be used by other requests.

    Args:
        connection: MicroStrategy REST API connection object.
        report_id (str): Unique ID of the report you wish to extract information from.
        offset (int, optional): Starting point within the collection of returned results. Default is 0.
        limit (int, optional): Used to control data extract behavior on datasets which have a large number of rows.
            The default is 1000. As an example, if the dataset has 50,000 rows, this function will incrementally
            extract all 50,000 rows in 1,000 row chunks. Depending on system resources, using a higher limit setting
            (e.g. 10,000) may reduce the total time required to extract the entire dataset.
        verbose (bool): Verbosity of request response; defaults to False.

    Returns:
        Complete HTTP response object.
    """

    response = connection.session.post(url=connection.base_url + '/api/v2/reports/' + report_id + '/instances/',
                                       json=body,
                                       params={'offset': offset,
                                               'limit': limit})
    if verbose:
        print(response.url)
    if not response.ok:
        response_handler(response, "Error getting report contents.")
    return response


def report_instance_id(connection, report_id, instance_id, offset=0, limit=5000, verbose=False):
    """
    Get the results of a previously created report instance, using the in-memory report instance created by a POST /api/reports/{reportId}/instances request.

    Args:
        connection: MicroStrategy REST API connection object
        report_id (str): Unique ID of the report you wish to extract information from.
        instance_id (str): Unique ID of the in-memory instance of a published report.
        offset (int): Optional. Starting point within the collection of returned results. Default is 0.
        limit (int): Optional. Used to control data extract behavior on datasets which have a large number of rows.
            The default is 1000. As an example, if the dataset has 50,000 rows, this function will incrementally
            extract all 50,000 rows in 1,000 row chunks. Depending on system resources, using a higher limit setting
            (e.g. 10,000) may reduce the total time required to extract the entire dataset.
        verbose (bool): Verbosity of request response; defaults to False

    Returns:
        Complete HTTP response object.
    """

    response = connection.session.get(url=connection.base_url + '/api/v2/reports/' + report_id + '/instances/' +
                                      instance_id,
                                      params={'offset': offset,
                                              'limit': limit})
    if verbose:
        print(response.url)
    if not response.ok:
        response_handler(response, "Error getting cube contents.", verbose=False)
    return response


def report_instance_id_coroutine(future_session, connection, report_id, instance_id, offset=0, limit=5000, verbose=False):
    """
    Get the future of a previously created instance for a specific report asynchroneously, using the in-memory instance created by report_instance().

    Returns:
        Complete Future object.

    """
    url = connection.base_url + '/api/v2/reports/' + report_id + '/instances/' + instance_id
    future = future_session.get(url, params={'offset': offset, 'limit': limit})
    if verbose:
        print(url)
    return future


def report_single_attribute_elements(connection, report_id, attribute_id, offset=0, limit=200000, verbose=False):
    """
    Get elements of a specific attribute of a specific report.

    Args:
        connection: MicroStrategy REST API connection object.
        report_id (str): Unique ID of the report you wish to extract information from.
        attribute_id (str): Unique ID of the attribute in the report.
        verbose (bool): Verbosity of request response; defaults to False.
    Returns:
        Complete HTTP response object
    """

    response = connection.session.get(url=connection.base_url + '/api/reports/' + report_id + '/attributes/' +
                                      attribute_id + '/elements',
                                      params={'offset': offset,
                                              'limit': limit})
    if verbose:
        print(response.url)
    if not response.ok:
        response_handler(response, "Error retrieving attribute " +
                         attribute_id + " elements")
    return response


def report_single_attribute_elements_coroutine(future_session, connection, report_id, attribute_id, offset=0, limit=200000,
verbose=False):
    """
    Get elements of a specific attribute of a specific report.

    Args:
        connection: MicroStrategy REST API connection object.
        report_id (str): Unique ID of the report you wish to extract information from.
        attribute_id (str): Unique ID of the attribute in the report.
    Returns:
        Complete Future object
    """
    url = connection.base_url + '/api/reports/' + report_id + '/attributes/' + attribute_id + '/elements'
    future = future_session.get(url, params={'offset': offset,
                                      'limit': limit})
    if verbose:
        print(url)
    return future
