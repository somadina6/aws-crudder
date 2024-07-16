SELECT 
    a.uuid,
    u.display_name,
    u.handle,
    a.message,
    a.created_at,
    a.expires_at 
FROM public.activities as a
INNER JOIN public.users as u ON a.user_uuid = u.uuid
WHERE 
    a.uuid = %(uuid_returned)s