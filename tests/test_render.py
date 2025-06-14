
def test_basic_render():
    import sqlrender

    # Define Bottle template

    template = """
    SELECT 
        name, age, role, gender 
    FROM 
        users
    WHERE 1 = 1
        % if ageMin:
        AND age >= {{ageMin}}
        % end
        AND role IN {{Util.join(roles)}}
    ORDER BY
        {{!orderBy}}
    LIMIT
        {{!limit}}
    """

    # Define input template parameters

    parameters = {
        'roles': ['Student', 'Graduate'],
        'ageMin': 18,
        'orderBy': 'name ASC',
        'limit': 100,
    }

    # Call render method

    sql_template, sql_params = sqlrender.render(template, parameters)

    print(sql_template)

    # Assert result template

    expected_sql_template = """
    SELECT 
        name, age, role, gender 
    FROM 
        users
    WHERE 1 = 1
        AND age >= ?
        AND role IN (?, ?)
    ORDER BY
        name ASC
    LIMIT
        100
    """

    assert expected_sql_template == sql_template

    # Assert result parameters

    expected_sql_params = (18, 'Student', 'Graduate')

    assert expected_sql_params == sql_params


def test_render():
    import sqlrender

    template = """
    SELECT 
        name, age, role, gender
    FROM 
        users
    WHERE 1 = 1
    % for user in users:
        AND (
            age > {{user['ageMin']}} 
            AND age <= {{user['ageMax']}}
            AND role IN {{Util.join(user['roles'])}}
            % if user['gender']:
            AND gender = {{user['gender']}}
            % end
        )
    % end
    ORDER BY
        {{!orderBy}}
    LIMIT
        {{!limit}}
    """
    params = {
        'users': [
            {'ageMin': 18, 'ageMax': 22, 'roles': ['Student', 'Graduate'], 'gender': 'female'},
            {'ageMin': 30, 'ageMax': 60, 'roles': None, 'gender': None},
        ],
        'limit': 100,
        'orderBy': 'name DESC'
    }

    result, param = sqlrender.render(template, params)
    # assert param == (15, 20, 'Graduate', 'Student', 30, 60)
    print(result, param)
