from db_gateway import db_gateway

def get_cleaned_id(pre_clean_data):
    if str(pre_clean_data)[0] == '<':
        if str(pre_clean_data)[2] == '&':
            return int(str(pre_clean_data)[3:-1])
        else:
            return int(str(pre_clean_data)[2:-1])
    else:
        return int(pre_clean_data)

    
def get_whether_in_vm_master(guild_id, channel_id):
    return True if db_gateway().get('voicemaster_master', params={'guild_id': guild_id, 'channel_id': channel_id}) else False
    # in_master = db_gateway().get('voicemaster_master', params={'guild_id': guild_id, 'channel_id': channel_id})
    # return bool(in_master)


def get_whether_in_vm_slave(guild_id, channel_id):
    return True if db_gateway().get('voicemaster_slave', params={'guild_id': guild_id, 'channel_id': channel_id}) else False
    # in_slave = db_gateway().get('voicemaster_slave', params={'guild_id': guild_id, 'channel_id': channel_id})
    # return bool(in_slave)


def user_is_timed_out(guild_id, user_id):
    return True if db_gateway().get('voicemaster_timeout', params={'guild_id': guild_id, 'user_id': user_id}) else False