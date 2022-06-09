using System;
using System.Globalization;
using DHI.Mike1D.Engine;
using DHI.Mike1D.Generic;
using DHI.Mike1D.Mike1DDataAccess;
using DHI.Mike1D.Plugins;
using DHI.Mike1D.StructureModule;

namespace Scripts
{
  public class MyScript
  {
    private IStructures _structures;
    private EngineNet _engineNet;

    private string _weirId = "Weir";
    private int _weirIndex;
    private double _crestWidthInitial;

    /// <summary> Method to modify MIKE 1D data. </summary>
    [Script]
    public void Initialize(Mike1DData mike1DData)
    {
      _structures = mike1DData.Network.StructureCollection.Structures;

      Console.WriteLine("Removing the weir");
      _weirIndex = _structures.FindIndex(x => x.ID == _weirId);
      var bcWeir = (BroadCrestedWeir)_structures[_weirIndex];
      _structures.RemoveAt(_weirIndex);

      Console.WriteLine("Creating Honma weir");
      var honmaWeir = CreateHonmaWeir(bcWeir);

      Console.WriteLine("Adding Honma weir to network");
      _structures.Add(honmaWeir);
    }

    private HonmaWeir CreateHonmaWeir(BroadCrestedWeir bcWeir)
    {
      _crestWidthInitial = bcWeir.WeirGeometry.LevelWidths[0].Width;

      var honmaWeir = new HonmaWeir
      {
        ID = bcWeir.ID,
        Location = bcWeir.Location,
        CrestWidth = _crestWidthInitial,
        CrestLevel = bcWeir.InvertLevelUpstream,
        WeirCoefficient = 1.0,
      };

      return honmaWeir;
    }

    /// <summary> Method to modify the controller. </summary>
    [Script]
    public void ModifyController(IMike1DController controller)
    {
      controller.ControllerEvent += ControllerOnControllerEvent;
    }

    private void ControllerOnControllerEvent(object sender, ControllerEventArgs e)
    {
      if (e.State != ControllerState.Running)
        return;

      var controller = (IMike1DController)sender;

      _engineNet = controller.EngineNet;
      _engineNet.PreTimeStepEvent += PreTimeStepEvent;
    }

    private void PreTimeStepEvent(DateTime timeN, DateTime timeNp1, int redoCount)
    {
      var honmaWeir = (HonmaWeir)_structures[_weirIndex];
      honmaWeir.CrestWidth = _crestWidthInitial * (1.0 - timeN.Minute/600.0);
      Console.WriteLine("Time: " + _engineNet.EngineTime.TimeNp1 + " Width: " + honmaWeir.CrestWidth);
    }
  }
}
