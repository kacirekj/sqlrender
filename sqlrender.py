from bottle import SimpleTemplate


class SqlTemplateUtil:
    @staticmethod
    def join(arr, open='(', separator=', ', close=')'):
        if arr is None or len(arr) == 0:
            res = SqlTemplate.doNotTrack
        elif isinstance(arr[0], str):
            res = separator.join('{{\'' + str(i) + '\'}}' for i in arr)
        else:
            res = separator.join('{{' + str(i) + '}}' for i in arr)
        res = open + res + close
        return res


class SqlTemplate:
    doNotTrack = "{{doNotTrack}}"

    def __init__(self, template, util=SqlTemplateUtil):
        self.sTemplate = SimpleTemplate(template)
        self.sTemplate._escape = self._escape_replacement
        self.sTemplate._str = self._str_replacement
        self.trackedParams = []
        self.util = util

    def render(self, *args, **kwargs):
        parametrized_sql_template = self.sTemplate.render(*args, **kwargs, Util=self.util)
        tracked_params = tuple(self.trackedParams)
        self.trackedParams = []
        return parametrized_sql_template, tracked_params

    @staticmethod
    def _is_nested_template(val):
        return isinstance(val, str) and '{{' in val and '}}' in val

    @staticmethod
    def _is_do_not_track(val):
        return isinstance(val, str) and SqlTemplate.doNotTrack in val

    def _escape_replacement(self, val):
        if val is None or self._is_do_not_track(val):
            res = val.replace(self.doNotTrack, '')
        elif self._is_nested_template(val):
            nested_sql_template, nested_tracked_params = SqlTemplate(val).render()
            self.trackedParams.extend(nested_tracked_params)
            res = nested_sql_template
        else:
            self.trackedParams.append(val)
            res = "?"
        return res

    def _str_replacement(self, val):
        if val is None:
            res = ""
        elif self._is_nested_template(val):
            val: str = val
            val = val.replace('{{', '')
            res = val.replace('}}', '')
        else:
            res = str(val)
        return res


def render(template, *args, **kwargs):
    return SqlTemplate(template).render(*args, **kwargs)
