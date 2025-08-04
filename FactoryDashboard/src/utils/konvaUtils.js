import Konva from 'konva';

export function createMachineShape(machineData) {
  const machineGroup = new Konva.Group({
    x: machineData.x,
    y: machineData.y,
    draggable: true,
  });

  const machineRect = new Konva.Rect({
    width: machineData.width,
    height: machineData.height,
    fill: machineData.status === 'Running' ? '#8fce00' : '#ff4d4d',
    stroke: '#555',
    strokeWidth: 2,
    cornerRadius: 8,
    shadowColor: 'black',
    shadowBlur: 10,
    shadowOpacity: 0.3,
    shadowOffsetX: 5,
    shadowOffsetY: 5,
  });

  const machineLabel = new Konva.Text({
    text: `${machineData.name}\nStatus: ${machineData.status}`,
    fontSize: 14,
    fontFamily: 'Arial, sans-serif',
    fill: '#fff',
    padding: 10,
    align: 'center',
    width: machineData.width,
  });

  machineGroup.add(machineRect);
  machineGroup.add(machineLabel);

  return machineGroup;
}
