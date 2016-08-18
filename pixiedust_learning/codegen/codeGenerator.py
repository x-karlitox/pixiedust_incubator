# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2016
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------
from pixiedust.display.display import *
import yaml
import requests

class PixieDustCodeGenDisplay(Display):
    def doRender(self, handlerId):

        self.addProfilingTime = False
        #hard code course for now, should come from cloudant later on
        courses=yaml.safe_load(self.renderTemplate("codeGen.json"))
        topic = self.options.get("topic")
        codesource = self.options.get("codesource")

        if topic is None:
            steps=[
                {"title": "Select the topic", "template": "selectTopic.html"},
                {"title": "Select the Code Snippet to generate", "template": "selectSnippet.html"},
                {"title": "Set Code Snippet variables", "template": "setVariables.html"}
            ]
            self._addHTMLTemplate("startWizard.html", courses=courses, steps=steps)
        elif codesource is None or codesource == "undefined":
            self._addHTMLTemplate("snippets/notAvailable.json")
        elif codesource.startswith("http"):
            r = requests.get(codesource)
            if r.status_code == requests.codes.ok:
                self._addHTML(r.text)
            else:
                self._addHTMLTemplate("snippets/notAvailable.json")
        else:
            self._addHTMLTemplate(codesource)