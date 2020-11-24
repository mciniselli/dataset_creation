'''
METHOD
| id                   |
| tokens               |
| repository           |
| commit               |
| url                  |

MASKED METHOD
| id                   |
| method_id            |
| masked_code          |
| mask                 |
| start                |
| end                  |
| constructtype        |
'''

from utils.input_output import read_file, write_file
import os


class Method:

    def __init__(self, code, repo, commit, url):
        self.code = code
        self.repo = repo
        self.commit = commit
        self.url = url
        self.tokens = self.get_list_of_tokens()
        self.start_conditions = None
        self.end_conditions = None
        self.conditon_types = None

    def read_indeces(self):
        index_method = 0
        index_masked = 0
        path_method = "result/id_method.txt"
        path_masked = "result/id_masked.txt"
        if os.path.exists(path_method) == False or os.path.exists(path_masked) == False:
            self.write_indeces("-1", "-1")
            return index_method, index_masked

        res = read_file(path_method)
        index_method = int(res[0])

        res = read_file(path_masked)
        index_masked = int(res[0])

        return index_method, index_masked

    def write_indeces(self, index_method, index_masked):
        path_method = "result/id_method.txt"
        path_masked = "result/id_masked.txt"

        write_file(path_method, [str(index_method)])
        write_file(path_masked, [str(index_masked)])

    def export_method_and_masked_method(self):

        if len(self.start_conditions) == 0:
            # print(self.code)
            return

        index_method, index_masked = self.read_indeces()
        method_filename = "result/methods.txt"
        masked_filename = "result/masked_methods.txt"

        separator = "|_|"

        index_method += 1
        method_fields = list()
        method_fields.append(str(index_method))
        method_fields.append(str(self.tokens))
        method_fields.append(self.repo)
        method_fields.append(self.commit)
        method_fields.append(self.url)

        record = separator.join(method_fields)
        write_file(method_filename, [record], "a+")

        records=list()

        for st, en, ct in zip(self.start_conditions, self.end_conditions, self.conditon_types):
            index_masked += 1
            masked_fields = list()
            masked_fields.append(str(index_masked))
            masked_fields.append(str(index_method))

            masked_code = ("".join(self.tokens[:st])).strip() + " <x>" + ("".join(self.tokens[en:])).strip()
            mask = ("".join(self.tokens[st:en])).strip() + "<z>"

            masked_fields.append(masked_code)
            masked_fields.append(mask)
            masked_fields.append(str(st))
            masked_fields.append(str(en))
            masked_fields.append(str(ct))

            record = separator.join(masked_fields)
            records.append(record)
        write_file(masked_filename, records, "a+")

        self.write_indeces(index_method, index_masked)

    def get_all_conditions(self):
        conditions = ["for", "if", "else if", "while"]
        conditions_value = ["FOR", "IF", "IF", "WHILE"]

        start_conditions = list()
        end_conditions = list()
        condition_types = list()

        for i, t in enumerate(self.tokens):
            if t in conditions:
                start_condition, end_condition = self.get_condition(i)
                start_conditions.append(start_condition)
                end_conditions.append(end_condition)

                found = False
                for i, c in enumerate(conditions):
                    if t == c:
                        condition_types.append(conditions_value[i])
                        found = True
                if found == False:
                    condition_types.append("NONE")

        self.start_conditions = start_conditions
        self.end_conditions = end_conditions
        self.conditon_types = condition_types

    def get_condition(self, index):
        start_index = index + 1
        tokens = self.tokens
        while tokens[start_index] != "(":
            start_index += 1
        start_index += 1
        end_index = -1
        num_brackets = 1
        for ind in range(start_index, len(tokens)):
            tt = tokens[ind]
            if tokens[ind] == "(":
                num_brackets += 1
            elif tokens[ind] == ")":
                num_brackets -= 1
            if num_brackets == 0:
                end_index = ind
                break

        # print("".join(tokens[start_index:end_index]))
        return start_index, end_index

    def get_list_of_tokens(self):
        tokens = self.code.split("|_|")  # sometimes there are spaces at the beginning and/or end (e.g. "throws ")
        tokens_fixed = list()
        for t in tokens:
            if len(t) == 0:
                continue
            if t == " ":
                tokens_fixed.append(t)
            elif t[0] == " " and t[-1] == " ":
                tokens_fixed.append(" ")
                tokens_fixed.append(t.strip())
                tokens_fixed.append(" ")

            elif t[0] == " ":
                tokens_fixed.append(" ")
                tokens_fixed.append(t.strip())
            elif t[-1] == " ":
                tokens_fixed.append(t.strip())
                tokens_fixed.append(" ")
            else:
                tokens_fixed.append(t)

        return tokens_fixed
