SELECT
    UPPER(ii.Serial) AS `serial`,
    ii2.MaxIn AS `downstream`,
    ii2.MaxOut AS `upstream`
FROM Equipment e
INNER JOIN InvItem ii ON ii.ID = e.InvItemID
INNER JOIN CustomerServices cs ON cs.CustomerID = e.EndUserID
INNER JOIN InternetInfo ii2 ON ii2.ServiceID = cs.ServiceID
WHERE e.DeviceType IN ('onu-ubnt', 'adtn-ont')
AND LENGTH(ii.Serial) = 12;