$('#member-search-form').submit(function(e) {
    console.log('Submitted member search form');
    e.preventDefault();

    const address = $(this).children('#address').val();
    console.log(`Address: ${address}`);
    const roles = $(this).children('#roles').val();
    console.log(`Roles: ${roles}`);

    const url = $(this).attr('action');
    console.log(`URL: ${url}`);

    $.ajax({
        url: url,
        type: 'GET',
        data: {
            'address': address,
            'roles': roles
        },
        success: function(response) {
            console.log('Successfully searched for my members!');
            console.log(response);
            for (var object in response) {
                createMember(response[object]);
            }
        },
        error: function(xhr, error, status) {
            console.log(`Error: ${error}, Status: ${status}`);
        }
    });
})

function createMember(object) {
    var container = $('#member-container');
    for (var key in object) {
        console.log(key, object[key]);
    };
    container.append(`
        <div member-id="${object.member_id}" class="card member">
            <a href=""><img class="card-img-top img-fluid rounded" src="${object.image}" ></a>
            <div class="card-body">
                <div class="card-title"<a href="${object.website}">${object.first_name} ${object.last_name}</a></div>
                <div class="card-text lead text-muted">${object.title}</div>
                <div class="card-text">Party: ${object.party}</div>
                <div class="card-text">State: ${object.state}</div>
                <div class="card-text">Office: ${object.office}</div>
                <div class="card-text">Phone #: ${object.phone}</div>
            </div>
        </div>
    `)
};