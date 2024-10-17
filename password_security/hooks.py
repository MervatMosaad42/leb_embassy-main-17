# Copyright 2024 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def post_init_hook(env):
    # Set password date for already existing users
    env.cr.execute(
        """
        UPDATE
            res_users
        SET
            password_write_date = NOW() at time zone 'UTC'
        WHERE
            password_write_date IS NULL;
    """
    )
