# Copyright 2011 The greplin-tornado-kissmetrics Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A kissmetrics API"""

import urllib
import functools
import logging
import time

from tornado import httpclient



class Kissmetrics(object):
  """A kissmetrics API"""

  BASE_URL = 'trk.kissmetrics.com'
  KM_EVENT = 'e'
  KM_ALIAS = 'a'
  KM_SET = 's'


  def __init__(self, api_key, user_id=None, use_https=True):
    self._api_key = api_key
    self._user_id = user_id
    self.BASE_URL = "https://" + self.BASE_URL if use_https else "http://" + self.BASE_URL


  def _call(self, command, params=None, callback=None):
    """Make a call to Kissmetrics"""
    params = params or {}
    callback = callback or (lambda (_): True)
    params['_k'] = self._api_key
    if '_t' in params:
      params['_d'] = 1
    else:
      params['_t'] = int(time.time())
    url = "%s/%s?%s" % (self.BASE_URL, command, urllib.urlencode(params))
    http = httpclient.AsyncHTTPClient()
    http.fetch(url, functools.partial(self._on_result, callback))


  def _on_result(self, callback, result):
    """Handle a result from kissmetrics"""
    if result.code != 200:
      logging.warning("Kissmetrics error: %s, %s", result.code, result.body)
      callback(False)
    callback(True)


  def alias(self, new, original=None):
    """Identify a user"""
    params = {
      '_p':original if original else self._user_id,
      '_n':new
    }
    self._call(self.KM_ALIAS, params)


  def event(self, name, **params):
    """Track an event"""
    params = params or {}
    params['_n'] = name
    params['_p'] = self._user_id
    self._call(self.KM_EVENT, params)

  def set(self, **params):
    params = params or {}
    params['_p'] = self._user_id
    self._call(self.KM_SET, params)









