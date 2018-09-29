// $('#member-search-form').submit(function(e) {
//     console.log('Submitted member search form');
//     e.preventDefault();
    
//     const address = $(this).children('#address').val();
//     console.log(`Address: ${address}`);
//     const roles = $(this).children('#roles').val();
//     console.log(`Roles: ${roles}`);

//     const url = $(this).attr('action');
//     console.log(`URL: ${url}`);

//     $.ajax({
//         url: url,
//         type: 'GET',
//         data: {
//             'address': address,
//             'roles': roles
//         },
//         success: function(response) {
//             console.log('Successfully searched for my members!');
//             console.log(response);
            
//             for (var object in response) {
//                 createMember(response[object]);
//             }
//         },
//         error: function(xhr, error, status) {
//             console.log(`Error: ${error}, Status: ${status}`);
//         }
//     });
// })

function createMember(object) {
    var container = $('#member-container');
    $('#member-container').empty();
    for (var key in object) {
        console.log(key, object[key]);
    };
    container.append(`
        <div member-id="${object.member_id}" class="member">
            <div class="row">
                <div class="col-md-3 member-image">
                    <img class="img-fluid rounded" src="${object.image}">
                    <hr>
                    <div class="email"><a href="${object.contact_page}">Email</a></div>
                    <div class="website"><a href="${object.website}">Website</a></div>
                </div>


                <div class="col-md-9 member-info">
                    <h4 class=""><a href="${object.website}">${object.first_name} ${object.last_name} (${object.party})</a></h4>
                    <div class="lead">${object.title}</div>
                    <div class="office">
                        <span class="member-label">Office:</span>
                        <span>${object.office}</span>
                    </div>
                    <div class="phone">
                        <span class="member-label">Phone:</span>
                        <span>${object.phone}</span>
                    </div>
                    <hr>
                    <div class="social-media">
                        <a href="https://www.twitter.com/${object.twitter_account}">
                            <img class="tw-icon" src="static/img/twitter-icon.png" alt="twitter">
                        </a>
                        <a href="https://www.facebook.com/${object.facebook_account}">
                            <img class="fb-icon" src="static/img/facebook-icon.png" alt="facebook">
                        </a>
                    </div>

                </div>
            </div>
        </div>
    `)
};