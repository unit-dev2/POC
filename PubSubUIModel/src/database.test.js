const db = require('./database');

beforeAll(async () => {
    await db.sequelize.sync({ force: true });
});

test('create device', async () => {
    expect.assertions(1);
    const device = await db.Device.create({
        id: 1,
        name: 'administracion',
        gcloudId: 'GDS218000ZE'
    });
    expect(device.id).toEqual(1);
});

test('get device', async () => {
    expect.assertions(2);
    const device = await db.Device.findByPk(1);
    expect(device.name).toEqual('administracion');
    expect(device.gcloudId).toEqual('GDS218000ZE');
});

test('delete devoce', async () => {
    expect.assertions(1);
    await db.Device.destroy({
        where: {
            id: 1
        }
    });
    const device = await db.Device.findByPk(1);
    expect(device).toBeNull();
});

afterAll(async () => {
    await db.sequelize.close();
});
