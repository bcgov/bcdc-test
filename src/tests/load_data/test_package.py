'''
Created on May 15, 2019

@author: KJNETHER

used to verify ability to create packages:

a) create org, retrieve id
    - do round crud test or org.
b) create package with org insert the org just created for this package.

'''

import pytest
import ckanapi
import requests
import pprint
import logging

logger = logging.getLogger(__name__)


def test_verify_test_package_org(create_get_org):
    logger.debug("got the org: %s", create_get_org)

def test_add_package(test_pkg_data, ckan_url, ckan_apitoken):
    '''
    
    2019-05-17 11:58:09 - 50 - test_package - DEBUG - return value: {u'sector': u'Natural Resources', u'preview_zoom_level': u'14', u'maintainer': None, u'west_bound_longitude': u'-139.5', u'iso_topic_string': u'imageryBaseMapsEarthCover', u'view_audience': u'Public', u'private': False, u'maintainer_email': None, u'num_tags': 4, u'east_bound_longitude': u'-113.5', u'id': u'ec15a9c5-e9e7-47aa-b133-ea645729453b', u'metadata_created': u'2019-05-17T18:58:04.599540', u'north_bound_latitude': u'60.0', u'metadata_modified': u'2019-05-17T18:58:04.599549', u'author': None, u'author_email': None, u'preview_map_service_url': u'https://openmaps.gov.bc.ca/geo/pub/WHSE_IMAGERY_AND_BASE_MAPS.AIMG_PHOTO_CENTROIDS_SP/ows?', u'preview_latitude': u'57.25894', u'object_name': u'WHSE_IMAGERY_AND_BASE_MAPS.AIMG_PHOTO_CENTROIDS_SP', u'state': u'active', u'version': None, u'link_to_imap': u'http://maps.gov.bc.ca/ess/hm/imap4m/?catalogLayers=6208,6344,6345,6346,6347,6348,6349,6350,6351,6352,6353,6354,6355,6356,6357,6358,6359,6360,6361,6362,6363,6364,6365,6366,6367,6368,6369,6370,6371,6372,6373,6374,6375,6376,6377,6378,6379,6380,6381,6382,6383,6384,6385,6386,6387,6388,6389,6390,6391,6392,6393,6394,6395,6396,6397&scale=100000.0&center=-14522083.9842,7813228.96005', u'relationships_as_object': [], u'license_id': u'22', u'type': u'Geographic', u'resources': [], u'details': [{u'data_precision': u'10', u'column_comments': u'AIRP_ID is the unique photo frame identifier, generated by the source APS system.', u'data_type': u'NUMBER', u'short_name': u'AIRP_ID', u'column_name': u'AIRP_ID'}, {u'data_precision': u'5', u'column_comments': u'FLYING_HEIGHT is the flying height above mean sea level in metres.', u'data_type': u'NUMBER', u'short_name': u'HEIGHT', u'column_name': u'FLYING_HEIGHT'}, {u'data_precision': u'4', u'column_comments': u'PHOTO_YEAR is the operational year to which this photograph is assigned.', u'data_type': u'NUMBER', u'short_name': u'YEAR', u'column_name': u'PHOTO_YEAR'}, {u'data_precision': u'7', u'column_comments': u'PHOTO_DATE is the date (year, month, and day) of exposure of the photograph.', u'data_type': u'DATE', u'short_name': u'DATE', u'column_name': u'PHOTO_DATE'}, {u'data_precision': u'20', u'column_comments': u'PHOTO_TIME is the time of exposure (hours, minutes, seconds), expressed in Pacific Standard Time, e.g., 9:43:09 AM.', u'data_type': u'VARCHAR2', u'short_name': u'TIME', u'column_name': u'PHOTO_TIME'}, {u'data_precision': u'8', u'column_comments': u'LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the location of the feature as measured from the equator, e.g., 55.323653.', u'data_type': u'NUMBER', u'short_name': u'LATITUDE', u'column_name': u'LATITUDE'}, {u'data_precision': u'9', u'column_comments': u'LONGITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the location of the feature as measured from the prime meridian, e.g., -123.093544.', u'data_type': u'NUMBER', u'short_name': u'LONGITUDE', u'column_name': u'LONGITUDE'}, {u'data_precision': u'20', u'column_comments': u'FILM_ROLL is a BC Government film roll identifier, e.g., bc5624.', u'data_type': u'VARCHAR2', u'short_name': u'FILM_ROLL', u'column_name': u'FILM_ROLL'}, {u'data_precision': u'10', u'column_comments': u'FRAME_NUMBER is the sequential frame number of this photograph within a film roll.', u'data_type': u'NUMBER', u'short_name': u'FRAME', u'column_name': u'FRAME_NUMBER'}, {u'data_precision': u'1', u'column_comments': u'GEOREF_METADATA_IND indicates if georeferencing metadata exists for this photograph, i.e., Y, N.', u'data_type': u'VARCHAR2', u'short_name': u'REFERENCED', u'column_name': u'GEOREF_METADATA_IND'}, {u'data_precision': u'1', u'column_comments': u"PUBLISHED_IND indicates if this photograph's geometry and metadata should be exposed for viewing, i.e., Y,N.", u'data_type': u'VARCHAR2', u'short_name': u'PUBLISHED', u'column_name': u'PUBLISHED_IND'}, {u'data_precision': u'100', u'column_comments': u'MEDIA describes the photographic medium on which this photograph was recorded, e.g. Film - BW.', u'data_type': u'VARCHAR2', u'short_name': u'MEDIA', u'column_name': u'MEDIA'}, {u'data_precision': u'100', u'column_comments': u'PHOTO_TAG is a combination of film roll identifier and frame number that uniquely identifies an air photo, e.g., bcc09012_035.', u'data_type': u'VARCHAR2', u'short_name': u'PHOTO_TAG', u'column_name': u'PHOTO_TAG'}, {u'data_precision': u'10', u'column_comments': u'BCGS_TILE identifies the BCGS mapsheet within which the centre of this photograph is contained. The BCGW mapsheet could be 1:20,000, 1:10,000 or 1:5,000, e.g., 104a01414.', u'data_type': u'VARCHAR2', u'short_name': u'BCGS_TILE', u'column_name': u'BCGS_TILE'}, {u'data_precision': u'10', u'column_comments': u'NTS_TILE identifies the NTS 1:50,000 mapsheet tile within which the centre of this photograph is contained, e.g., 104A03.', u'data_type': u'VARCHAR2', u'short_name': u'NTS_TILE', u'column_name': u'NTS_TILE'}, {u'data_precision': u'10', u'column_comments': u'SCALE of the photo with respect to ground based on a 9-inch square hardcopy print, e.g., 1:18,000.', u'data_type': u'VARCHAR2', u'short_name': u'SCALE', u'column_name': u'SCALE'}, {u'data_precision': u'5', u'column_comments': u'GROUND_SAMPLE_DISTANCE indicates the distance on the ground in centimetres represented by a single pixel in the scanned or original digital version of this photograph.', u'data_type': u'NUMBER', u'short_name': u'GSD', u'column_name': u'GROUND_SAMPLE_DISTANCE'}, {u'data_precision': u'20', u'column_comments': u'OPERATION_TAG is an alpha numeric shorthand operation identifier representing photographic medium, operation number, requesting agency and operational year of photography, e.g., D003FI15.', u'data_type': u'VARCHAR2', u'short_name': u'OPER_TAG', u'column_name': u'OPERATION_TAG'}, {u'data_precision': u'10', u'column_comments': u'FOCAL_LENGTH is the focal length of the lens, in millimetres, used to capture this photograph.', u'data_type': u'NUMBER', u'short_name': u'FOC_LEN', u'column_name': u'FOCAL_LENGTH'}, {u'data_precision': u'500', u'column_comments': u'THUMBNAIL_IMAGE_URL is a hyperlink to the 1/16th resolution thumbnail version of this image.', u'data_type': u'VARCHAR2', u'short_name': u'THMBNL_MGL', u'column_name': u'THUMBNAIL_IMAGE_URL'}, {u'data_precision': u'500', u'column_comments': u'FLIGHT_LOG_URL is a hyperlink to the scanned version of the original handwritten flight log page (film record) for this image.', u'data_type': u'VARCHAR2', u'short_name': u'LOG_URL', u'column_name': u'FLIGHT_LOG_URL'}, {u'data_precision': u'500', u'column_comments': u'CAMERA_CALIBRATION_URL is a hyperlink to the camera calibration report file for this image.', u'data_type': u'VARCHAR2', u'short_name': u'CALIB_URL', u'column_name': u'CAMERA_CALIBRATION_URL'}, {u'data_precision': u'500', u'column_comments': u'PATB_GEOREF_URL is a hyperlink to the PatB geo-referencing file for this image.', u'data_type': u'VARCHAR2', u'short_name': u'PATB_URL', u'column_name': u'PATB_GEOREF_URL'}, {u'data_precision': u'10', u'column_comments': u'FLIGHT_LINE_SEGMENT_ID identifies the section of flight line to which this photograph belongs.', u'data_type': u'NUMBER', u'short_name': u'FLGHT_L_ID', u'column_name': u'FLIGHT_LINE_SEGMENT_ID'}, {u'data_precision': u'10', u'column_comments': u'OPERATION_ID is a unique identifier for the operation to which this photograph belongs. It may be used by the data custodian to diagnose positional errors.', u'data_type': u'NUMBER', u'short_name': u'OPER_ID', u'column_name': u'OPERATION_ID'}, {u'data_precision': u'10', u'column_comments': u'FILM_RECORD_ID is a unique identifier for the film record to which this photograph belongs. It may be used by the data custodian to diagnose positional errors.', u'data_type': u'NUMBER', u'short_name': u'FIRE_ID', u'column_name': u'FILM_RECORD_ID'}, {u'data_precision': u'1', u'column_comments': u'SHAPE is the column used to reference the spatial coordinates defining the feature.', u'data_type': u'SDO_GEOMETRY', u'short_name': u'SHAPE', u'column_name': u'SHAPE'}, {u'data_precision': u'38', u'column_comments': u'OBJECTID is a column required by spatial layers that interact with ESRI ArcSDE. It is populated with unique values automatically by SDE.', u'data_type': u'NUMBER', u'short_name': u'OBJECTID', u'column_name': u'OBJECTID'}, {u'data_precision': u'4000', u'column_comments': u'SE_ANNO_CAD_DATA is a binary column used by spatial tools to store annotation, curve features and CAD data when using the SDO_GEOMETRY storage data type.', u'data_type': u'BLOB', u'short_name': u'ANNO_CAD', u'column_name': u'SE_ANNO_CAD_DATA'}], u'num_resources': 0, u'object_short_name': u'PHOTO_CENT', u'tags': [{u'vocabulary_id': None, u'state': u'active', u'display_name': u'aerial imagery', u'id': u'd00abc18-6aa7-4ec5-ab00-7c151937e611', u'name': u'aerial imagery'}, {u'vocabulary_id': None, u'state': u'active', u'display_name': u'airphoto centers', u'id': u'0955937c-a65f-4216-92e4-23efc9450f34', u'name': u'airphoto centers'}, {u'vocabulary_id': None, u'state': u'active', u'display_name': u'airphoto centroids', u'id': u'81ab1c49-15f8-4d72-8267-f83d36da3f24', u'name': u'airphoto centroids'}, {u'vocabulary_id': None, u'state': u'active', u'display_name': u'imagery', u'id': u'89e41f71-3095-4cff-9d82-92035ae14e85', u'name': u'imagery'}], u'spatial': u'{"type": "Polygon", "coordinates": [[[-139.5, 48.0], [-139.5, 60.0], [-113.5, 60.0], [-113.5, 48.0], [-139.5, 48.0]]]}', u'resource_status': u'unkwan', u'south_bound_latitude': u'48.0', u'record_archive_date': u'', u'layer_name': u'WHSE_IMAGERY_AND_BASE_MAPS.AIMG_PHOTO_CENTROIDS_SP', u'groups': [], u'creator_user_id': u'4225f7dc-8e24-486d-a6e3-a456d0577d0c', u'download_audience': u'Public', u'org': u'GeoBC', u'object_table_comments': u'Annual layers of photo centre points and associated metadata representing air photos in the Provincial air photo imagery inventory.', u'relationships_as_subject': [], u'license_title': u'Access Only', u'security_class': u'LOW-PUBLIC', u'organization': {u'description': u'GeoBC creates and manages geospatial information and products to help better manage natural resources in British Columbia. GeoBC also offers consultation services across all natural resource sector agencies.\r\n\r\nGeoBC has four areas of focus directly tied to natural resource business functions:\r\n\r\n1. Creating and maintaining a standard set of base spatial data that is open and accessible\r\n1. Providing direction and assurance for provincial land registries\r\n1. Offering Crown land and resource research expertise to other government agencies\r\n1. Delivering a service for custom solutions to natural resource business issues\r\n\r\nLearn how GeoBC supports B.C.\u2019s resource management and environmental stewardship objectives:\r\n\r\n1. GeoBC Plan (PDF)\r\n1. GeoBC Overview & Promotional Package (PDF)\r\nServices', u'created': u'2014-10-19T11:50:45.726045', u'title': u'GeoBC', u'name': u'geobc', u'is_organization': True, u'state': u'active', u'image_url': u'', u'revision_id': u'803b16e0-a5fb-4b80-8175-a20f232e57c4', u'type': u'organization', u'id': u'052617ff-8a1e-4d41-b5b5-0f64c9a9e6ff', u'approval_status': u'approved'}, u'name': u'airphoto-centroids-test', u'isopen': False, u'preview_longitude': u'-130.4541', u'url': None, u'metadata_visibility': u'Public', u'notes': u'__A set of points representing the centre points of all individual air photo frames catalogued in the provincial collection, dating back to 1963.__\r\n\r\n', u'owner_org': u'052617ff-8a1e-4d41-b5b5-0f64c9a9e6ff', u'edc_state': u'PUBLISHED', u'license_url': u'http://www2.gov.bc.ca/gov/content/home/copyright', u'title': u'Airphoto Centroids', u'revision_id': u'6e5e2c69-59b8-466e-9ce9-b4181c49bdff'}

    '''
    pkgName = test_pkg_data['name']
    logger.debug("apitoken: %s", len(ckan_apitoken))
    remoteApi = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)   
    #pkgShow = remoteApi.action.package_show(id=pkgName)
    #logger.debug("pkgShow: %s", pkgShow)
    pkgList = remoteApi.action.package_list()
    
    # TODO: need a better way to verify that the package does not exist as 
    #      package list will not be up to date until the indexer run.
    #      should use package_show to determine if the object exists in 
    #      bcdc / ckan.
    
#     grps = remoteApi.action.group_list()
#     for grp in grps:
#         logger.debug('grp: %s', grp)
#         
#     raise
    
    if pkgName in pkgList:
        # remove so can be re-added
        # could also add this to a wrapper fixture that gets called
        # at start and end of everything here.  Leaving it here for
        # now
        logger.debug("cleaning up package: %s", pkgName)
        remoteApi.action.package_delete(pkgName)
    logger.debug("adding the package: %s", pkgName)
    # above line not working but posting anyways as want to share the 
    # skeleton code asap
    try:
        logger.debug("trying to add...")
        pkg_create = remoteApi.action.package_create(**test_pkg_data)
        logger.debug("return value: %s", pkg_create)
        url = '{0}/{1}'.format(ckan_url, 'api/3/action/edc_package_update')
        header = {'X-CKAN-API-KEY': ckan_apitoken,
                  'content-type': 'application/json;charset=utf-8'}
        logger.debug("trying to call package update")
        #r = requests.post(url, headers=header, json=test_pkg_data)
        #logger.debug("r: %s %s", r.text, r.status_code)
        
        
        
    except Exception as e:
        logger.debug("error: %s", e)
        raise e
    logger.debug("finished adding record")
    