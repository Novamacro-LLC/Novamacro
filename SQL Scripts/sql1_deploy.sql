-- Add product_type data

insert into public.internal_producttype (name, description)
    VALUES ('Website Design'    ,'Website Design and Hosting'   ),
           ('Digital Marketing' ,'Digital Marketing Tools'      );

-- Add product data

insert into public.internal_product (name, description, price, payment_link, product_type_id)
    VALUES ('Essential Website Package',
            'Website Design and Hosting',
            5.00,
            'https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-d776feb852e94e9f96627d7d4bc9b01539f865587cfb4d0a93fd0f2a43247f4741fefe48521643759206b487ab382f21?locale=EN_US',
            1),
           ('Growth Website Package',
            'Website Design, Hosting with Marketing Tools',
            10.00,
            'https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-58ea02449ff34a7d9e57aa8ba48750eebbb5c14071c94e9198060c4e25b14ee4ba11a09f26f7419c9552b600b3c54d27?locale=EN_US',
            1),
            ('Premium Website Package',
             'Website, Design, Hosting, Marketing Tools and Enhanced Support',
             25.00,
             'https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-d181c2419121483eb667fcc495cea8a8ac526c94738043dea7eeeac26d81207030bc1d814bec4c7e8c1fa0dbe22071fb?locale=EN_US',
             1),
            ('Essential Digital Marketing Package',
             'Social Media Manager',
             5.00,
             'https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-92fe022d2bfc4eb79e890a5334367f2d9a85d63cbd374e1f92dd602caaa5c72828828909b5734dc8a72daf5a7da6da67?locale=EN_US',
             2),
            ('Growth Digital Marketing Package',
             'Social Media Manager with website integration',
             10.00,
             'https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-a979e36bccd848eca71c44a2097c66986677f97e0b724916aa5a19c635d57e9e6a604a295b1d466daed40cf39a2bc814?locale=EN_US',
             2),
            ('Premium Digital Marketing Package',
             'Social Media Manager, Website Integration, with enhanced support',
             25.00,
             'https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-4a418a8d35054cf3afcb7b23753080a30d348fabd75447a2ac29703282fadfd7b74f7feda0424b40b4d6c61a3667d754?locale=EN_US',
             2);